import base64, gzip, hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

def read(path):
    return json.loads(path.read_text())

version = read(ROOT/'package.json')['version']
coverage = read(ROOT/'data/coverage.json')
groups = []
for label in read(ROOT/'data/countries.json'):
    code = label['id']
    stats = coverage['byCountry'][code]
    places = read(ROOT/f'data/cities/{code}.json')
    divisions = {}
    for region in read(ROOT/f'data/regions/{code}.json'):
        title=region['zh'] or region['en']
        divisions[region['id']]=title
        for child in region.get('children',[]):
            divisions[child['id']]=title+' / '+(child['zh'] or child['en'])
    assert len(places)==stats['cities']
    groups.append({**label,'stats':stats,'divisions':divisions,'places':places})
archive = ROOT/f'artifacts/winrisef-world-cities-{version}.tgz'
land = [ring for f in read(HERE/'land.geojson')['features'] for ring in f['geometry']['coordinates']]
data = {'land':land,'groups':groups,'version':version,'sha':hashlib.sha256(archive.read_bytes()).hexdigest()}
packed = base64.b64encode(gzip.compress(json.dumps(data,ensure_ascii=False,separators=(',',':')).encode(),mtime=0)).decode()
args = sys.argv[1:]
globe = '--globe' in args
if globe:
    args.remove('--globe')
page = (HERE/('globe-template.html' if globe else 'map-template.html')).read_text().replace('%PAYLOAD%',packed)
label = '交互地球' if globe else '交互核查地图'
path = Path(args[0]).expanduser() if args else Path.home()/'Downloads'/f'世界城市{label}-{version}.html'
path.write_text(page)
print(path)
