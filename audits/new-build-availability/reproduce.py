"""Audit field availability in the public Q3 sales aggregate. Python standard library."""
import argparse,csv,json,hashlib
from collections import Counter
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--output',type=Path,default=Path('reproduced'));a=p.parse_args()
rows=list(csv.DictReader(a.source.open(newline='')))
keys=[(r['geography'],r['quarter']) for r in rows]
assert len(keys)==len(set(keys)), 'Duplicate geography-quarter'
assert all(r['source_lag_affected'] in ('True','False') for r in rows)
assert all(r['new_build_share_pct']=='' or 0<=float(r['new_build_share_pct'])<=100 for r in rows)
a.output.mkdir(parents=True,exist_ok=True)
status=Counter((r['new_build_share_pct']=='',r['source_lag_affected']=='True') for r in rows)
result={'source_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),'rows':len(rows),'geographies':len(set(r['geography'] for r in rows)),'quarters':len(set(r['quarter'] for r in rows)),'new_build_share_blank':sum(r['new_build_share_pct']=='' for r in rows),'lag_true':sum(r['source_lag_affected']=='True' for r in rows),'share_present_lag_false':status[(False,False)],'share_blank_lag_false':status[(True,False)],'share_blank_lag_true':status[(True,True)],'share_present_lag_true':status[(False,True)],'method':'Count blank strings and exact boolean strings separately; no imputation, transaction weighting or independence assumption.'}
(a.output/'audit-summary.json').write_text(json.dumps(result,indent=2)+'\n')
with (a.output/'field-availability-by-quarter.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['quarter','geography_quarter_rows','new_build_share_present_rows','new_build_share_withheld_rows','lag_flag_true_rows','withheld_share_and_lag_false_rows'])
 for q in sorted(set(r['quarter'] for r in rows)):
  rs=[r for r in rows if r['quarter']==q]
  w.writerow([q,len(rs),sum(r['new_build_share_pct']!='' for r in rs),sum(r['new_build_share_pct']=='' for r in rs),sum(r['source_lag_affected']=='True' for r in rs),sum(r['new_build_share_pct']=='' and r['source_lag_affected']=='False' for r in rs)])
print(json.dumps(result,indent=2))
