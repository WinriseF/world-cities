"""Check a packed release against original national files and export the audit ledger."""
import csv
import json
import re
import sys
import tarfile
import unicodedata
from pathlib import Path

from bs4 import BeautifulSoup
import xlrd


def normalize(name):
    return ''.join(c for c in unicodedata.normalize('NFKD', name.casefold()) if c.isalnum())


package, registers, output = map(Path, sys.argv[1:])
with tarfile.open(package) as archive:
    def read(file):
        return json.load(archive.extractfile('package/data/' + file + '.json'))
    countries = read('countries')
    by_country = read('coverage')['byCountry']
    cities = {c['id']: read('cities/' + c['id']) for c in countries}
    parents = {c['id']: {r['id']: r for r in read('regions/' + c['id'])} for c in countries}

# Coordinates and names for PL came from PRNG. TERYT provides an independent code and name list.
sheet = xlrd.open_workbook(registers / 'pl-tablica_kts-teryt_2026.xls', on_demand=True).sheet_by_name('Gminy 2026')
expected = {}
for row in range(1, sheet.nrows):
    code, _, label = sheet.row_values(row)[:3]
    if code[-1:] in ('1', '4'):
        expected[code] = re.sub(r'( - miasto)? \([14]\)$', '', label)
assert len(expected) == len(cities['PL']) == 1026
for c in cities['PL']:
    code = c['officialId']
    assert parents['PL'][c['region']]['code'] == 'PL-' + code[:2]
    assert expected.pop(code) in [c['en'], *c.get('aliases', [])], (code, c['en'])
assert not expected

features = json.loads((registers / 'id-big-kabkota.json').read_bytes())['features']
rows = [f['attributes'] for f in features if f['attributes']['tipadm'] == 5]
expected = {r['kdpkab']: r for r in rows}
assert len(rows) == len(expected) == len(cities['ID']) == 98
for c in cities['ID']:
    r = expected.pop(c['officialId'])
    assert r['wadmkk'] in [c['en'], *c.get('aliases', [])]
    province = r['wadmpr'].replace('Daerah Istimewa Yogyakarta', 'DI Yogyakarta')
    assert parents['ID'][c['region']]['en'] == province
assert not expected

cn = {}
for p in json.loads((registers / 'cn-tree.json').read_bytes())['data']['children']:
    if not p['code'].isdigit() or int(p['code']) > 65:
        continue
    if p['type'] == '直辖市':
        cn['cn:' + p['code'].ljust(6, '0')] = (p['name'].removesuffix('市'), p['name'], 'municipality')
    for child in p['children'] or []:
        if child['level'] == 2 and child['type'] in ('地级市', '自治州', '盟', '地区'):
            cn['cn:' + child['code'].ljust(6, '0')] = (
                child['name'].removesuffix('市'), p['name'], 'city' if child['type'] == '地级市' else 'prefecture')
actual = {c['id']: (c['zh'], parents['CN'][c['region']]['zh'], c['kind']) for c in cities['CN']
          if parents['CN'][c['region']]['code'] not in {'CN-HK', 'CN-MO', 'CN-TW'}}
assert cn == actual and len(cn) == 337

doc = BeautifulSoup((registers / 'gb.html').read_bytes(), 'html.parser')
territories = {'Isle of Man': 'IM', 'Bermuda': 'BM', 'Gibraltar': 'GI', 'Falkland Islands': 'FK', 'Saint Helena': 'SH'}
parts = {'England', 'Scotland', 'Northern Ireland', 'Wales'}
aliases = {'Derry': 'Londonderry', 'City of Westminster': 'Westminster', 'Saint Asaph': 'St Asaph',
           'Saint Davids': 'St Davids', 'Brighton and Hove': 'Brighton & Hove'}
seen = set()
for heading in doc.select('main h4'):
    area = heading.get_text(strip=True)
    if area not in territories and area not in parts:
        continue
    expected = sorted(normalize(li.get_text(strip=True).strip('*').removeprefix('City of '))
                      for li in heading.find_next('ul').select('li'))
    if area in parts:
        group = [c for c in cities['GB'] if parents['GB'][c['region']]['en'] == area]
    else:
        group = cities[territories[area]]
    actual = sorted(normalize(aliases.get(c['en'], c['en'])) for c in group)
    assert expected == actual, (area, set(expected) ^ set(actual))
    seen.add(area)
assert seen == parts | territories.keys()
with output.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['地区码', '国家或地区', '状态', '包内记录', '参考名录应收', '参考范围', '版本', '来源'])
    labels = {'partial': '部分已核对', 'reference-checked': '已逐项核对指定名录', 'pending': '待核实', 'not-applicable': '不适用'}
    for country in countries:
        cc = country['id']
        item = by_country[cc]['cityReference']
        if item['status'] == 'not-applicable':
            assert not cities[cc], cc
        writer.writerow([cc, country['zh'], labels[item['status']], len(cities[cc]), item.get('expected'),
                         item.get('scope'), item.get('edition'), item.get('source')])
print('PL, ID, CN, GB and five UK territory/dependency lists matched; wrote', len(countries), 'jurisdictions')
