"""Prepare Indonesian Kota and Polish miasto records from the national registers."""
import gzip
import json
import math
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

root = Path(__file__).resolve().parents[2]
registers = Path(sys.argv[1])
csc = root / '.cache/csc'
states = {r['id']: r for r in json.loads((csc / 'regions.json').read_bytes())}
cities = json.load(gzip.open(csc / 'cities.json.gz'))
wiki_names = json.loads((root / 'sources/wikidata-names.json').read_bytes())
wiki_cities = json.load(gzip.open(root / 'sources/wikidata-city-status.json.gz'))


def norm(name):
    return ''.join(c for c in unicodedata.normalize('NFKD', name.casefold()) if c.isalnum())


def province(row):
    state = states[row['state_id']]
    while str(state['level']) != '1' and state['parent_id']:
        state = states[int(state['parent_id'])]
    return state['iso3166_2']


def lookup_name(cc, name):
    if cc == 'ID':
        name = re.sub(r'^Kota (?:Adm\. )?| City$', '', name, flags=re.I)
        if norm(name) == 'padangsidimpuan':
            name = 'Padangsidempuan'
    return norm(name)


index = defaultdict(dict)
for row in cities:
    cc = row['country_code']
    if cc == 'PL' and row['type'] in ('municipality', 'adm1', 'adm2', 'district'):
        continue
    if cc in ('PL', 'ID'):
        tr = row['translations'] or {}
        for alias in [row['name'], row['native'], tr.get('pl' if cc == 'PL' else 'id')]:
            if alias:
                index[cc, province(row), lookup_name(cc, alias)][row['id']] = row


def record(cc, code, state, name, xy=None, zh=None, en=None):
    matches = list(index[cc, state, lookup_name(cc, name)].values())
    if xy:
        def distance(r):
            dy = float(r['latitude']) - xy[0]
            dx = (float(r['longitude']) - xy[1]) * math.cos(math.radians(xy[0]))
            return math.hypot(dx, dy) * 111.2
        matches = sorted((r for r in matches if distance(r) < 8), key=distance)
        if len(matches) > 1 and distance(matches[1]) - distance(matches[0]) < 0.5:
            matches = []
    else:
        if len(matches) > 1:
            matches = [r for r in matches if r['type_local'] == 'kota']
        assert len(matches) == 1, (cc, code, name, [r['name'] for r in matches])
    row = matches[0] if matches else {}
    tr = row.get('translations') or {}
    if not xy:
        xy = float(row['latitude']), float(row['longitude'])
    label = en or tr.get('en') or row.get('name') or name
    res = dict(code=code, state=state, en=label, name=name, lat=xy[0], lon=xy[1])
    if row:
        res['csc'] = row['id']
    qid = row.get('wikiDataId')
    chinese = zh or tr.get('zh-CN') or wiki_names.get(qid) or wiki_cities.get(qid)
    if not isinstance(chinese, str):
        chinese = None
    if chinese:
        res['zh'] = chinese
    if label != name:
        res['aliases'] = [name]
    return res


def polish():
    rows = []
    labels = json.loads((root / 'sources/poland-labels.json').read_bytes())
    doc = ElementTree.parse(registers / 'pl-prng.gml')
    for city in doc.iterfind('.//{*}M1_UrzedoweNazwyMiejscowosci'):
        assert city.findtext('{*}RODZAJOBIEKTU') == 'miasto'
        code = city.findtext('{*}IDENTYFIKATORGMINY')
        # For a mixed gmina the register gives the whole unit (3).
        # TERYT separately identifies the city within it with suffix 4.
        assert code[-1] in '13'
        code = code[:-1] + ('4' if code.endswith('3') else '1')
        name = city.findtext('{*}NAZWAGLOWNA')
        point = city.find('.//{*}Point')
        assert point.attrib['srsName'] == 'urn:ogc:def:crs:EPSG::4326'
        xy = tuple(map(float, point.findtext('{*}pos').split()))
        assert 49 <= xy[0] < 55 and 14 <= xy[1] < 25
        simc = city.findtext('{*}IDENTYFIKATORSIMC')
        item = record('PL', code, 'PL-' + code[:2], name, xy, labels.get(simc, {}).get('zh'))
        if name == 'Warszawa':
            item['capital'] = True
            item.setdefault('aliases', []).append('M. st. Warszawa')
        rows.append(item)
    return rows


def indonesian():
    # Geonames populated places or the municipal seat, with names reviewed on Wikidata.
    supplements = {
        '11.75': ('6713355', 'Subulussalam', '苏布鲁萨兰'),
        '13.73': ('1628472', 'Sawahlunto', '沙哇伦多'),
        '71.72': ('1648637', 'Bitung', '比通'),
        '74.72': ('1649541', 'Baubau', '巴务巴务市'),
        '82.72': ('1623951', 'Tidore Islands', '蒂多雷'),
    }
    with ZipFile(registers / 'id-geonames.zip') as archive:
        required = {v[0] for v in supplements.values()}
        points = {}
        for line in archive.open('ID.txt'):
            f = line.decode().split('\t')
            if f[0] in required:
                assert f[6] == 'P' and f[8] == 'ID'
                points[f[0]] = (float(f[4]), float(f[5]))
    provinces = {norm(r['name']): r['iso3166_2'] for r in states.values()
                 if r['country_code'] == 'ID' and str(r['level']) == '1'}
    provinces['daerahistimewayogyakarta'] = 'ID-YO'
    rows = []
    doc = json.loads((registers / 'id-big-kabkota.json').read_bytes())
    assert not doc.get('exceededTransferLimit')
    for feature in doc['features']:
        r = feature['attributes']
        if r['tipadm'] != 5:
            continue
        code, name = r['kdpkab'], r['wadmkk']
        assert name.startswith('Kota ') and code[:2] == r['kdppum']
        state = provinces[norm(r['wadmpr'])]
        if code in supplements:
            gid, en, zh = supplements[code]
            item = record('ID', code, state, name, points[gid], zh, en)
        else:
            item = record('ID', code, state, name)
        rows.append(item)
    return rows


output = {'ID': indonesian(), 'PL': polish()}
for cc, rows in output.items():
    rows.sort(key=lambda r: r['code'])
    ids = [r['csc'] for r in rows if 'csc' in r]
    assert len(ids) == len(set(ids)) and len(rows) == len({r['code'] for r in rows})
    print(cc, len(rows), 'Chinese labels', sum('zh' in r for r in rows), 'linked CSC', len(ids))
encoded = json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
(root / 'sources/id-pl-cities.json.gz').write_bytes(gzip.compress(encoded, mtime=0))
