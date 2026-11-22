"""Build complete province/status shards from extraction fixtures, excluding city and postal code."""
from pathlib import Path
import json,gzip,hashlib,collections
from decimal import Decimal
BASE=Path(__file__).resolve().parents[1]/'.cache';OUT=BASE/'donation-starter';OUT.mkdir(exist_ok=True)
summary={'year':'2023','scope':'Registered party annual returns, all published rows; submitted and reviewed versions kept separate','captured_at':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'shards':[],'entities':{},'sources':[],'aggregates':[]}
for version in ['submitted','reviewed']:
 meta=json.loads((BASE/f'ec-{version}-2023-metadata.json').read_text());summary['sources'].append({k:meta[k] for k in ['source','source_sha256','version','year','rows']})
 data=json.load(gzip.open(BASE/f'ec-{version}-2023-annual.json.gz','rt'));ix={k:i for i,k in enumerate(data['headers'])}
 provinces=collections.defaultdict(list);occurrences=collections.Counter();agg={}
 for values in data['rows']:
  def value(field):return values[ix[field]]
  monetary=int(Decimal(value('Monetary amount') or '0')*100);nonmonetary=int(Decimal(value('Non-Monetary amount') or '0')*100);cents=monetary+nonmonetary
  province=value('Contributor Province') or 'UNKNOWN';entity=value('Recipient');entity_id=value('Recipient ID');part=value('Part Number of Return');kind='directed' if 'Directed' in value('Financial Report part') else 'ordinary'
  core={'entity_id':entity_id,'entity':entity,'period':value('Fiscal/Election date'),'province':province,'contributor':value('Contributor name'),'date':value('Contribution Received date') or None,'amount':cents/100,'monetary':monetary/100,'nonmonetary':nonmonetary/100,'part':part,'kind':kind,'cohort':entity_id+'|'+value('Fiscal/Election date')+'|'+value('Form ID')+'|'+part,'directed_to':value('Leadership contestant') or None}
  fingerprint=hashlib.sha256(json.dumps(core,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()[:24];occurrences[fingerprint]+=1
  row={'id':version+':'+fingerprint+':'+str(occurrences[fingerprint]),'version':version,**core,'source':meta['source']}
  provinces[province].append(row);summary['entities'][entity_id]=entity
  key=(version,province,entity_id,kind)
  if key not in agg:agg[key]={'version':version,'province':province,'entity_id':entity_id,'entity':entity,'kind':kind,'rows':0,'amount_cents':0,'monetary_cents':0,'nonmonetary_cents':0,'distribution':collections.Counter()}
  a=agg[key];a['rows']+=1;a['amount_cents']+=cents;a['monetary_cents']+=monetary;a['nonmonetary_cents']+=nonmonetary
  bucket=next((name for upper,name in [(0,'negative'),(2000,'0–19.99'),(10000,'20–99.99'),(20000,'100–199.99'),(50000,'200–499.99'),(100000,'500–999.99'),(200000,'1000–1999.99')] if cents<upper),'2000+')
  a['distribution'][bucket]+=1
 summary['aggregates']+=list(agg.values())
 for province,rows in sorted(provinces.items()):
  filename=f'{version}-{province}.json.gz'
  raw=json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode()
  (OUT/filename).write_bytes(gzip.compress(raw,mtime=0));summary['shards'].append({'version':version,'province':province,'file':filename,'count':len(rows),'bytes':len(raw),'compressed_bytes':(OUT/filename).stat().st_size,'sha256':hashlib.sha256(raw).hexdigest()})
 summary.setdefault('exact_duplicate_public_rows',{})[version]=sum(n-1 for n in occurrences.values())
(OUT/'manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'total':sum(s['count'] for s in summary['shards']),'compressed_mb':round(sum(s['compressed_bytes'] for s in summary['shards'])/1e6,2),'shards':len(summary['shards']),'duplicates':summary['exact_duplicate_public_rows']}))
