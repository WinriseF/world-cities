"""Check the packed JSON against the independent national registers."""
from pathlib import Path
from openpyxl import load_workbook
from zipfile import ZipFile
from tarfile import open as open_tar
import csv, json, sys
path, ref = map(Path, sys.argv[1:3])
checks={}
with open_tar(path) as t:
 def data(path):return json.load(t.extractfile('package/data/'+path+'.json'))
 tab={}
 for cc in ['US','BR','DE','JP','PH']:
  regions={s['id']:(s['code'] or s['en']) for s in data('regions/'+cc)}
  lst=data('cities/'+cc)
  tab[cc]={c['officialId']:regions[c['region']] for c in lst if c.get('officialId')}
  assert len(tab[cc])==sum(c.get('officialId') is not None for c in lst)
 def compare(cc,pairs):
  assert len(pairs)==len(dict(pairs))
  a={code:parent for code,parent in pairs}
  diffs=[c for c,rg in a.items() if tab[cc].get(c)!=rg]
  assert not diffs,(cc,diffs[:5])
  checks[cc]=dict(officialRequired=len(a),matchedWithCorrectRegion=len(a),otherOfficialCodes=len(tab[cc])-len(a))
 z=ZipFile(ref/'us.zip');rs=csv.DictReader(z.read(z.namelist()[0]).decode().splitlines(),delimiter='|')
 compare('US',[(r['GEOID'],'US-'+r['USPS']) for r in rs if r['USPS']!='PR' and r['LSAD']=='25' and r['FUNCSTAT'] in ['A','B']])
 compare('BR',[(str(r['municipio-id']),'BR-'+r['UF-sigla']) for r in json.loads((ref/'br.json').read_bytes()) if r['municipio-id'] not in [5300108,2605459]])
 de_states='SH HH NI HB NW HE RP BW BY SL BE BB MV SN ST TH'.split()
 de=load_workbook(ref/'de.xlsx',read_only=True,data_only=True)['Städte']
 compare('DE',[(r[1][:5]+r[1][-3:],'DE-'+de_states[int(r[1][:2])-1]) for r in de.values if len(str(r[1]))==12 and str(r[1]).isdigit()])
 jp=load_workbook(ref/'jp.xlsx',read_only=True,data_only=True).worksheets[0]
 compare('JP',[(r[0],'JP-'+r[0][:2]) for r in jp.values if r[2] and r[2].endswith('市')])
 ph_states={'01':'PH-01','02':'PH-02','03':'PH-03','04':'PH-40','05':'PH-05','06':'PH-06','07':'PH-07','08':'PH-08','09':'PH-09','10':'PH-10','11':'PH-11','12':'PH-12','13':'PH-00','14':'PH-15','16':'PH-13','17':'PH-41','18':'Negros Island Region','19':'PH-14'}
 compare('PH',[(k,ph_states[k[:2]]) for k in json.loads((ref/'ph.json').read_bytes())])
 assert len(data('regions/AO'))==21 and len(data('regions/BI'))==5 and len(data('regions/FR'))==18
 assert all(c['region'] is not None for c in data('cities/BI'))
 assert {c['zh'] for c in data('cities/CN') if c['region']=='csc:r:2264'}=={'拉萨','日喀则','昌都','林芝','山南','那曲','阿里地区'}
 assert not any('/.cache/' in s or '/artifacts/' in s for s in t.getnames())
 print(json.dumps(checks));print('package bytes',path.stat().st_size,'data totals',data('coverage')['totals'])
