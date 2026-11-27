"""Compare mainland cities and the three provincial areas with the Tianditu layer."""
import argparse
import json
import tarfile
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import Point, shape

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('package', type=Path)
parser.add_argument('geojson', type=Path)
args = parser.parse_args()

with tarfile.open(args.package) as archive:
    regions = json.load(archive.extractfile('package/data/regions/CN.json'))
    cities = json.load(archive.extractfile('package/data/cities/CN.json'))
layer = json.loads(args.geojson.read_bytes())
transform = Transformer.from_crs('EPSG:4326', layer['crs']['properties']['name'], always_xy=True)

# The download has one province-level polygon per area for Taiwan, Hong Kong and Macao.
province_codes = {'CN-TW': '710000', 'CN-HK': '810000', 'CN-MO': '820000'}
province_by_region = {r['id']: province_codes[r['code']] for r in regions if r['code'] in province_codes}
other_areas = {'629700', '629800', '629900'}
areas = {}
for feature in layer['features']:
    if feature['geometry']['type'] not in ('Polygon', 'MultiPolygon'):
        continue
    props = feature['properties']
    gb = props['gb']
    if not (len(gb) == 9 and gb.startswith('156') and gb.isdigit()):
        raise ValueError(f'Unexpected Tianditu area code {gb!r}')
    code = gb[3:]
    if code in other_areas or not code.endswith('00'):  # County-level units have a nonzero suffix.
        continue
    if code in areas:
        raise ValueError(f'Duplicate Tianditu area {code}')
    areas[code] = (props['name'].removesuffix('市'), shape(feature['geometry']))

province_areas = {code: areas.pop(code) for code in province_codes.values()}
errors = []
province_points = 0
for city in cities:
    province = province_by_region.get(city['region'])
    if province:
        name, boundary = province_areas[province]
        if not boundary.covers(Point(*transform.transform(city['lon'], city['lat']))):
            errors.append(f"{city['id']} {city['zh']}: point outside {name}")
        province_points += 1
        continue
    code = city['id'].removeprefix('cn:')
    area = areas.pop(code, None)
    if area is None:
        errors.append(f"{code} {city['zh']}: missing or duplicate area match")
        continue
    name, geometry = area
    if name != city['zh']:
        errors.append(f"{code}: package {city['zh']!r}, Tianditu {name!r}")
    if not geometry.covers(Point(*transform.transform(city['lon'], city['lat']))):
        errors.append(f'{code} {name}: point outside its boundary')
errors.extend(f'{code} {name}: missing package record' for code, (name, _) in areas.items())
if errors:
    raise SystemExit('\n'.join(errors))
print(f'{len(cities) - province_points} mainland codes, names and points matched; '
      f'{province_points} points matched to their province-level boundaries.')
