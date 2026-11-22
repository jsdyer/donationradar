from common import ROOT,save,fetch,sha
import json,argparse,subprocess,sys,shutil

def main():
 p=argparse.ArgumentParser();p.add_argument('--seed',action='store_true');a=p.parse_args();cache=ROOT/'.cache';cache.mkdir(exist_ok=True)
 if not a.seed:
  for version,suffix in [('submitted','de'),('reviewed','audt')]:
   url=f'https://www.elections.ca/fin/oda/od_cntrbtn_{suffix}_e.zip';(cache/f'ec-{version}.zip').write_bytes(fetch(url,limit=400_000_000));subprocess.run([sys.executable,str(ROOT/'scripts/extract_ec.py'),version,'2023'],check=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/normalize_ec.py')],check=True)
 path=cache/'donation-starter';meta=json.loads((path/'manifest.json').read_text());shards=[]
 for shard in meta['shards']:
  source=path/shard['file'];raw=source.read_bytes();digest=sha(raw);dest=ROOT/'archive/shards'/f'{digest}.json.gz';dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():
   with dest.open('xb') as output:output.write(raw)
  shards.append({**shard,'file':dest.relative_to(ROOT).as_posix()})
 records=[]
 for r in meta['aggregates']:
  row=dict(r);row['id']='|'.join(str(r[k]) for k in ['version','province','entity_id','kind']);row['shard_sha256']=next(s['sha256'] for s in shards if s['version']==r['version'] and s['province']==r['province']);records.append(row)
 sources=[{'label':s['version'].title()+' contribution ZIP','url':s['source'],'sha256':s['source_sha256']} for s in meta['sources']]
 sources.append({'label':'Elections Canada political financing open data','url':'https://www.elections.ca/content.aspx?section=fin&dir=oda&document=index&lang=e'})
 save(records,sources=sources,coverage=f"Complete published 2023 registered-party annual cohort · {sum(s['count'] for s in shards):,} submitted/reviewed records · province shards",warnings=['Submitted and reviewed versions are separate; never add them together. Ordinary and directed contributions are separate.','These are disclosed contribution records, not unique donors or total party revenue. Similar names do not establish the same person.'],extra={'source_shards':shards,'aggregates':records,'year':'2023','total_records':sum(s['count'] for s in shards),'exact_duplicate_public_rows':meta['exact_duplicate_public_rows']})
if __name__=='__main__':main()
