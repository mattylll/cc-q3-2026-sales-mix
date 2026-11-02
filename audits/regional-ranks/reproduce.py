"""Reproduce the regional-rank comparison from frozen public aggregates.

Standard-library-only calculations. Optional --chart requires matplotlib.
Source statistics are retained, not recalculated from transactions.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
NATIONAL = 'England and Wales'

def write_csv(path, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=BASE / 'derived')
    parser.add_argument('--chart', action='store_true')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    source = BASE / 'recorded_sales.csv'
    data = list(csv.DictReader(source.open()))
    assert len(data) == 120
    assert len({(r['geography'], r['quarter']) for r in data}) == 120
    periods = ['2025-Q3', '2026-Q3']
    selected = {q: {r['geography']: r for r in data if r['quarter'] == q} for q in periods}
    assert all(len(v) == 8 for v in selected.values())
    geos = [g for g in selected[periods[0]] if g != NATIONAL]
    assert len(geos) == 7 and set(selected[periods[0]]) == set(selected[periods[1]])
    med = {q: {g: float(selected[q][g]['median_price_gbp']) for g in selected[q]} for q in periods}
    ranks = {q: {g: 1 + sum(med[q][other] > med[q][g] for other in geos) for g in geos} for q in periods}
    rows = []
    for g in sorted(geos, key=lambda g: ranks[periods[1]][g]):
        a,b = (med[q][g] for q in periods)
        rows.append(dict(geography=g, median_2025_q3_gbp=a, median_2026_q3_gbp=b,
            rank_2025_q3=ranks[periods[0]][g], rank_2026_q3=ranks[periods[1]][g],
            rank_change=ranks[periods[0]][g]-ranks[periods[1]][g],
            median_difference_gbp=b-a, median_difference_pct=100*(b/a-1),
            difference_from_national_2026_gbp=b-med[periods[1]][NATIONAL],
            difference_from_national_2026_pct=100*(b/med[periods[1]][NATIONAL]-1),
            recorded_transactions_2025_q3=int(selected[periods[0]][g]['transactions_recorded']),
            recorded_transactions_2026_q3=int(selected[periods[1]][g]['transactions_recorded'])))
    spans = {q: max(med[q][g] for g in geos)-min(med[q][g] for g in geos) for q in periods}
    summary = dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        source_edition='2026-10-05', latest_transaction_date='2026-08-28',
        regional_groups=7, unchanged_ranks=sum(r['rank_change']==0 for r in rows),
        national_median_2026_q3_gbp=med['2026-Q3'][NATIONAL],
        span_2025_q3_gbp=spans['2025-Q3'], span_2026_q3_gbp=spans['2026-Q3'],
        span_difference_gbp=spans['2026-Q3']-spans['2025-Q3'],
        median_falls=sum(r['median_difference_gbp']<0 for r in rows),
        median_unchanged=sum(r['median_difference_gbp']==0 for r in rows),
        q3_2026_national_records=int(selected['2026-Q3'][NATIONAL]['transactions_recorded']),
        q3_2026_mapped_records=sum(r['recorded_transactions_2026_q3'] for r in rows))
    assert summary['unchanged_ranks'] == 7
    assert summary['span_2026_q3_gbp'] == 225000
    assert summary['span_2025_q3_gbp'] == 245005
    assert summary['median_falls'] == 5 and summary['median_unchanged'] == 2
    assert summary['q3_2026_national_records'] - summary['q3_2026_mapped_records'] == 14
    assert rows[0]['difference_from_national_2026_gbp'] == 130000
    assert rows[-1]['difference_from_national_2026_gbp'] == -95000
    write_csv(args.output / 'regional_rank_comparison.csv', rows)
    write_csv(args.output / 'selected_source_rows.csv', [selected[q][g] for q in periods for g in selected[q]])
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    if args.chart:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter
        plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12})
        fig, ax = plt.subplots(figsize=(13,8), facecolor='#F5F4EF')
        ax.set_facecolor('#F5F4EF')
        for i,r in enumerate(rows):
            a,b = r['median_2025_q3_gbp'],r['median_2026_q3_gbp']
            ax.plot([a,b],[i,i], color='#849098', lw=3, zorder=1)
            ax.scatter(a,i,s=110,facecolors='#F5F4EF',edgecolors='#7D8992',linewidths=2,zorder=2)
            ax.scatter(b,i,s=70,color='#087F78',zorder=3)
            ax.annotate(f"£{b:,.0f}",(b,i),xytext=(0,-19),textcoords='offset points',ha='center',fontsize=11,color='#123047')
        ax.set_yticks(range(7),[r['geography'].replace(' & ',' &\n') for r in rows])
        ax.invert_yaxis();ax.set_ylim(6.65,-.6);ax.set_xlim(175000,475000)
        ax.axvline(295000, color='#B56432', ls=':', lw=1.6)
        ax.text(299000,6.42,'£295,000 national median\nQ3 2026 snapshot',color='#995022',fontsize=10,va='center')
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'£{x/1000:,.0f}k'))
        ax.grid(axis='x',alpha=.18);ax.tick_params(length=0,pad=10)
        for s in ax.spines.values():s.set_visible(False)
        fig.text(.05,.95,'Same regional order. Different price benchmarks.',fontsize=23,weight='bold',color='#123047')
        fig.text(.05,.90,'Seven custom reporting groups | Q3 2025 versus provisional Q3 2026',fontsize=13,color='#485962')
        ax.scatter([],[],s=100,facecolors='#F5F4EF',edgecolors='#7D8992',label='Q3 2025')
        ax.scatter([],[],s=70,color='#087F78',label='Q3 2026 provisional')
        ax.legend(loc='lower right',bbox_to_anchor=(1,1.015),ncol=2,frameon=False,fontsize=10)
        fig.text(.05,.07,'Retained aggregate medians, not a constant-quality price index or scheme valuation.',fontsize=11,color='#123047')
        fig.text(.05,.035,'Construction Capital | HMLR-derived snapshot frozen 5 Oct 2026. Latest transaction: 28 Aug; September absent.',fontsize=10,color='#485962')
        fig.subplots_adjust(left=.23,right=.97,top=.83,bottom=.18)
        fig.savefig(args.output / 'regional-ranks.png',dpi=160,facecolor=fig.get_facecolor())
        plt.close(fig)
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    main()
