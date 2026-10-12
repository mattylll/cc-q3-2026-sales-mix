"""Reproduce a four-category mix-distance analysis. Python 3.9+, stdlib only."""
import csv, json, math, argparse
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parent
TYPES=('D','F','S','T')
def load_groups():
    source=list(csv.DictReader((ROOT/'property_mix.csv').open(newline='')))
    totals={(r['geography'],r['quarter']):r for r in csv.DictReader((ROOT/'recorded_sales.csv').open(newline=''))}
    grouped=defaultdict(dict)
    for r in source:
        key=(r['geography'],r['quarter']);t=r['property_type']
        assert t not in grouped[key]
        grouped[key][t]=int(r['transactions_recorded'])
    result=[]
    for (g,q),counts in grouped.items():
        assert set(counts)==set(TYPES)
        n=sum(counts.values());assert n==int(totals[(g,q)]['transactions_recorded']) and n>0
        shares={t:100*counts[t]/n for t in TYPES}
        assert math.isclose(sum(shares.values()),100,abs_tol=1e-9)
        result.append({'geography':g,'quarter':q,'count':n,'counts':counts,'shares':shares,'provisional':q=='2026-Q3','lag_flag':totals[(g,q)]['source_lag_affected']=='True'})
    assert len(source)==480 and len(result)==120
    return result

def distance(a,b):
    changes={t:b['shares'][t]-a['shares'][t] for t in TYPES}
    d=sum(abs(x) for x in changes.values())/2
    assert -1e-9<=d<=100+1e-9
    assert math.isclose(d,sum(max(x,0) for x in changes.values()),abs_tol=1e-9)
    return {'first_geography':a['geography'],'first_quarter':a['quarter'],'second_geography':b['geography'],'second_quarter':b['quarter'],'first_count':a['count'],'second_count':b['count'],'mix_distance_pp':round(d,6),**{f'{t}_share_change_pp':round(changes[t],6) for t in TYPES}}

def calculate(groups):
    lookup={(r['geography'],r['quarter']):r for r in groups}
    national=lookup[('England and Wales','2026-Q3')]
    regional=[distance(national,r) for r in groups if r['quarter']=='2026-Q3' and r['geography']!='England and Wales']
    annual=[distance(lookup[(r['geography'],'2025-Q3')],r) for r in groups if r['quarter']=='2026-Q3']
    return regional,annual

def write_tables(out):
    out.mkdir(parents=True,exist_ok=True);groups=load_groups();regional,annual=calculate(groups)
    for name,rows in [('regional_mix_distances.csv',regional),('annual_mix_distances.csv',annual)]:
        with (out/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/'data.json').write_text(json.dumps(groups,indent=2)+'\n')
    return groups,regional,annual
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'reproduced');args=parser.parse_args()
    g,r,a=write_tables(args.output);print(json.dumps({'compositions':len(g),'regional_comparisons':len(r),'annual_comparisons':len(a),'output':str(args.output)}))
