"""Extraction proof: public EC annual party returns; never read the entire CSV into memory."""
import csv,io,zipfile,json,collections,gzip,sys,time,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]/'.cache'
VERSION=sys.argv[1];YEAR=sys.argv[2] if len(sys.argv)>2 else '2023'
HEADERS=['Recipient ID','Recipient','Political Party of Recipient','Fiscal/Election date','Form ID','Financial Report','Part Number of Return','Financial Report part','Contributor type','Contributor name','Contributor Province','Contribution Received date','Monetary amount','Non-Monetary amount','Contribution given through','Leadership contestant']
rows=[];counts=collections.Counter();annual=collections.Counter();date_min=None;date_max=None;started=time.time()
with zipfile.ZipFile(BASE/f'ec-{VERSION}.zip') as z:
 with io.TextIOWrapper(z.open(z.namelist()[0]),encoding='utf-8-sig',newline='') as f:
  reader=csv.reader(f);source_headers=next(reader);ix={k:i for i,k in enumerate(source_headers)}
  for r in reader:
   if r[ix['Political Entity']]!='Registered parties':continue
   report=r[ix['Financial Report']]
   if 'Quarterly' in report:continue
   fiscal=r[ix['Fiscal/Election date']]
   annual[(fiscal[:4],report)]+=1
   if fiscal[:4]!=YEAR:continue
   vals=[r[ix[k]].strip() for k in HEADERS]
   rows.append(vals);counts[vals[10]]+=1
meta={'source':'https://www.elections.ca/fin/oda/od_cntrbtn_'+('audt' if VERSION=='reviewed' else 'de')+'_e.zip','source_sha256':hashlib.file_digest((BASE/f'ec-{VERSION}.zip').open('rb'),'sha256').hexdigest(),'version':VERSION,'year':YEAR,'headers':HEADERS,'rows':len(rows),'provinces':dict(counts),'all_annual_years':[{'year':k[0],'report':k[1],'rows':v} for k,v in sorted(annual.items())],'seconds':round(time.time()-started)}
(BASE/f'ec-{VERSION}-{YEAR}-metadata.json').write_text(json.dumps(meta,indent=2))
with gzip.open(BASE/f'ec-{VERSION}-{YEAR}-annual.json.gz','wt',encoding='utf-8') as out:json.dump({'headers':HEADERS,'rows':rows},out,ensure_ascii=False,separators=(',',':'))
print(json.dumps(meta),flush=True)
