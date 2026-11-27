"""Build the frozen national city rosters from official files (see SOURCES.md)."""
import csv
import gzip
import json
import math
import re
import sqlite3
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile
from tarfile import open as open_tar

from openpyxl import load_workbook

root = Path(__file__).resolve().parents[2]
registers, enrichment = map(Path, sys.argv[1:3])
states = json.loads((root / '.cache/csc/regions.json').read_bytes())
raw = json.loads(gzip.decompress((root / '.cache/csc/cities.json.gz').read_bytes()))
parents = {r['id']: r for r in states}
extra_labels = json.loads((root/'sources/wikidata-names.json').read_bytes())
han = re.compile(r'[\u3400-\u9fff]')
rosters = defaultdict(list)
missing = []

def norm(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', (value or '').casefold()) if c.isalnum())

def value(literal):
    return json.loads(literal.rsplit('@', 1)[0]) if literal.startswith('"') else ''

def first_han(*values):
    return next((s for s in values if s and han.search(s)), None)

def state_key(row):
    state = parents.get(row['state_id'])
    while state and state.get('level') != '1':
        state = parents.get(int(state['parent_id'] or 0))
    return state and (state['iso3166_2'] or state['name'])

def distance(a, b):
    lat, lon = a
    other_lat, other_lon = b
    dx = (other_lon - lon + 180) % 360 - 180
    return 111.2 * math.hypot(lat-other_lat, dx*math.cos(math.radians((lat+other_lat)/2)))

def raw_point(row):
    return float(row['latitude']), float(row['longitude'])

by_name, by_entity = defaultdict(list), defaultdict(list)
langs = {'BR':'pt', 'US':'en', 'DE':'de', 'JP':'ja', 'PH':'en'}
for row in raw:
    cc = row['country_code']
    if cc not in langs:
        continue
    if row['wikiDataId']:
        by_entity[cc, row['wikiDataId']].append(row)
    names = {row['name'], row['native'], (row['translations'] or {}).get(langs[cc])}
    for name in filter(None, names):
        by_name[cc, state_key(row), norm(name)].append(row)

def wiki_index(cc):
    result = defaultdict(list)
    for line in (enrichment / (cc+'.tsv')).read_text().splitlines()[1:]:
        key, uri, point, hans, zh, en = line.split('\t')
        qid = uri.rsplit('/', 1)[1].strip('>')
        coords = re.fullmatch(r'POINT\(([-\d.]+) ([-\d.]+)\)', point)
        xy = (float(coords[2]),float(coords[1])) if coords else None
        result[value(key).replace('-', '')].append((qid, xy, first_han(value(hans), value(zh)), value(en)))
    return result

reviewed_aliases = {
    ('US','0602112'):['Angels Camp'], ('US','2005337'):['Bellaire'], ('US','2146027'):['Lexington-Fayette'],
    ('US','4873493'):['Pecos'], ('DE','09671111'):['Alzenau in Unterfranken'],
    ('DE','09773136'):['Gundelfingen'], ('DE','09275154'):['Vilshofen'], ('DE','06635004'):['Battenberg'],
    ('DE','06413000'):['Offenbach'], ('DE','03254043'):['Gronau'], ('DE','05154008'):['Emmerich'],
    ('DE','05117000'):['Mülheim'], ('DE','05958044'):['Sundern'], ('DE','07316000'):['Neustadt'],
    ('DE','14626030'):['Bernstadt'], ('DE','14523340'):['Reichenbach/Vogtland'], ('DE','15081240'):['Kalbe']
}
indices = {cc:wiki_index(cc) for cc in langs}
# Prefer an existing public ID when the upstream gazetteer has duplicate entries.
previous_names = {}
preview = root/'artifacts/winrisef-world-cities-0.1.0.tgz'
if preview.exists():
    with open_tar(preview) as package:
        for cc in langs:
            rows=json.load(package.extractfile(f'package/data/cities/{cc}.json'))
            previous_names.update((int(r['id'][4:]),r) for r in rows if r['id'].startswith('csc:'))
else:
    for cc in langs:
        rows=json.loads((root/'data/cities'/f'{cc}.json').read_bytes())
        previous_names.update((int(r['id'][4:]),r) for r in rows if r['id'].startswith('csc:'))
earth = {f['properties']['WIKIDATAID']: (f['properties']['LATITUDE'],f['properties']['LONGITUDE'])
         for f in json.loads((root/'.cache/csc/world-places.geojson').read_bytes())['features']}

used_raw = set()
def add(cc, code, state, name, *, point=None, keys=(), alternatives=(), english=None, capital=False):
    names = [name, *alternatives, *reviewed_aliases.get((cc,code), [])]
    variants = {norm(v) for v in names}
    evidence = {}
    name_agrees = {}
    for key in (code, *keys):
        for qid, coord, zh, en in indices[cc].get(key, []):
            if norm(en) in variants:
                name_agrees[qid] = zh or extra_labels.get(qid)
            if point and coord and distance(point,coord)>35:
                # Gazetteer interior points can be offshore or far from the urban seat.
                witnesses = [raw_point(r) for r in by_entity[cc,qid]]
                if qid in earth:
                    witnesses.append(earth[qid])
                if norm(en) not in variants or not any(distance(coord,w)<10 for w in witnesses):
                    continue
            evidence[qid] = (coord, zh, en)
    # A historical code may be reused. Prefer the matching name and nearest point.
    def rank(item):
        coord, _, en = item[1]
        return (norm(en) not in variants, distance(point,coord) if point and coord else math.inf)
    ranked = sorted(evidence.items(), key=rank)
    wd = ranked[0] if ranked and (len(ranked)==1 or rank(ranked[0]) < rank(ranked[1])) else None
    qid, (wd_point, wd_zh, wd_en) = wd or (None, (None, None, None))
    anchor = wd_point or point
    candidates = {}
    if qid:
        candidates.update((r['id'],r) for r in by_entity[cc,qid])
    for alias in names+[wd_en]:
        if alias:
            candidates.update((r['id'],r) for r in by_name[cc,state,norm(alias)])
    def score(r):
        return (not (qid and qid==r['wikiDataId']), state_key(r)!=state,
                r['id'] not in previous_names, norm(r['name']) not in variants,
                distance(raw_point(r),anchor) if anchor else 0, r['id'])
    linked = None
    for r in sorted(candidates.values(),key=score):
        same_place = qid and r['wikiDataId']==qid and state_key(r)==state and norm(r['name']) in variants
        if r['id'] in used_raw or (anchor and distance(anchor,raw_point(r))>35 and not same_place):
            continue
        if not (qid and r['wikiDataId'] == qid) and state_key(r)!=state:
            continue
        linked = r
        break
    coords = point or wd_point or (linked and raw_point(linked))
    if point and wd_point and distance(point,wd_point)>15 and qid in earth and distance(wd_point,earth[qid])<10:
        coords = wd_point
    if point and wd_point and linked and qid==linked['wikiDataId'] and distance(wd_point,raw_point(linked))<10:
        coords = wd_point
    if not coords:
        missing.append((cc,code,name,'point'))
        return
    translations = (linked or {}).get('translations') or {}
    label = english or wd_en or translations.get('en') or (linked or {}).get('name') or name
    if not re.search('[a-zA-ZÀ-ž]', label):
        missing.append((cc,code,name,'English'))
        return
    code_label = next(iter(name_agrees.values())) if len(name_agrees)==1 else None
    chinese = wd_zh or extra_labels.get(qid) or code_label or first_han(translations.get('zh-CN'), translations.get('zh'))
    record = dict(code=code, state=state, en=label, name=name, lat=round(coords[0],6), lon=round(coords[1],6))
    previous = linked and previous_names.get(linked['id'])
    aliases = [name, *reviewed_aliases.get((cc,code),[])]
    if previous:
        aliases.extend((previous['en'],previous['zh']))
    record['aliases'] = sorted({v for v in aliases if v and v not in (label,chinese)})
    if not record['aliases']:
        del record['aliases']
    if chinese:
        record['zh'] = chinese
    if linked:
        record['csc'] = linked['id']
        used_raw.add(linked['id'])
    if capital:
        record['capital'] = True
    rosters[cc].append(record)

with ZipFile(registers/'us.zip') as archive:
    places = list(csv.DictReader(archive.read(archive.namelist()[0]).decode('utf-8-sig').splitlines(), delimiter='|'))
# Keep the federal capital and urban places represented as consolidated governments.
consolidated = {
    'Anchorage municipality':'Anchorage', 'Milford city (balance)':'Milford',
    'Athens-Clarke County unified government (balance)':'Athens',
    'Augusta-Richmond County consolidated government (balance)':'Augusta',
    'Macon-Bibb County':'Macon', 'Indianapolis city (balance)':'Indianapolis',
    'Lexington-Fayette urban county':'Lexington', 'Butte-Silver Bow (balance)':'Butte',
    'Anaconda-Deer Lodge County':'Anaconda', 'Carson City':'Carson City',
    'Nashville-Davidson metropolitan government (balance)':'Nashville', 'Ranson corporation':'Ranson'
}
for row in places:
    state, name, lsad = row['USPS'], row['NAME'], row['LSAD']
    if state=='PR':
        continue
    if lsad=='25' and row['FUNCSTAT'] in ('A','B','N'):
        label=name.removesuffix(' city')
    elif lsad=='53':
        label=name.removesuffix(' city and borough')
    elif name in consolidated:
        label=consolidated[name]
    elif row['GEOID'] in {'2650660','2279240','4843132','4871756','4875236'}:
        label=name.rsplit(' ',1)[0]
    else:
        continue
    add('US',row['GEOID'],'US-'+state,label,english='Washington D.C.' if state=='DC' else label,
        alternatives=[name],point=(float(row['INTPTLAT']),float(row['INTPTLONG'])),capital=state=='DC')

db=sqlite3.connect((enrichment/'br-points.gpkg').resolve().as_uri()+'?mode=ro',uri=True)
seats={code:(lat,lon) for code,lat,lon in db.execute(
    "SELECT CD_MUN,LAT_LOCALIDADE,LONG_LOCALIDADE FROM BR_localidades_2022 WHERE CT_LOCALIDADE='Cidade'")}
for row in json.loads((registers/'br.json').read_bytes()):
    code=str(row['municipio-id'])
    if code=='2605459':
        continue
    add('BR',code,'BR-'+row['UF-sigla'],row['municipio-nome'],point=seats[code],
        english=row['municipio-nome'],capital=code=='5300108')

de_states='SH HH NI HB NW HE RP BW BY SL BE BB MV SN ST TH'.split()
sheet=load_workbook(registers/'de.xlsx',read_only=True,data_only=True)['Städte']
for r in sheet.values:
    ars=str(r[1])
    if ars.isdigit() and len(ars)==12:
        code=ars[:5]+ars[-3:]
        name=r[2].split(',')[0].strip()
        add('DE',code,'DE-'+de_states[int(ars[:2])-1],name,keys=['06415000'] if code=='06435014' else [],
            alternatives=name.split('/'),capital=code=='11000000')

add('DE','09184123','DE-BY','Haar')  # Granted city status in January 2025.

jp=load_workbook(registers/'jp.xlsx',read_only=True,data_only=True).worksheets[0]
for code,_,name,*_ in jp.values:
    if name and name.endswith('市'):
        add('JP',code,'JP-'+code[:2],name,alternatives=[name[:-1]])

ph_states={'01':'PH-01','02':'PH-02','03':'PH-03','04':'PH-40','05':'PH-05','06':'PH-06',
           '07':'PH-07','08':'PH-08','09':'PH-09','10':'PH-10','11':'PH-11','12':'PH-12',
           '13':'PH-00','14':'PH-15','16':'PH-13','17':'PH-41','18':'Negros Island Region','19':'PH-14'}
old=json.loads((enrichment/'ph-codes.json').read_bytes())
for code,name in json.loads((registers/'ph.json').read_bytes()).items():
    bare=re.sub(r'^City of ','',name,flags=re.I)
    add('PH',code,ph_states[code[:2]],name,keys=[old[code]],alternatives=[bare,bare+' City'],
        english=bare,capital=code=='1380600000')

target=root/'sources/official-cities.json.gz'
for cc,rows in rosters.items():
    assert len({r['code'] for r in rows})==len(rows)
    rows.sort(key=lambda r:r['code'])
    print(cc,len(rows),'Chinese',sum('zh' in r for r in rows),'linked CSC',sum('csc' in r for r in rows))
payload=json.dumps(rosters,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
if missing:
    raise ValueError(missing)
target.write_bytes(gzip.compress(payload,mtime=0))
