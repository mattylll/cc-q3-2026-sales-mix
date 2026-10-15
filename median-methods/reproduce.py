"""Reproduce median-summary diagnostics with Python 3 standard library only.

Run from an unpacked package: python reproduce.py --output reproduced
Source medians are retained, not recomputed from transaction-level records.
"""
import argparse
import csv
from pathlib import Path
from statistics import mean, median


def calculate(root):
    with (root / 'recorded_sales.csv').open(newline='') as f:
        source = list(csv.DictReader(f))
    with (root / 'regional_mapping_coverage.csv').open(newline='') as f:
        coverage = {r['quarter']: r for r in csv.DictReader(f)}
    results = []
    for q in sorted({r['quarter'] for r in source}):
        national, = [r for r in source if r['quarter'] == q and r['geography'] == 'England and Wales']
        regions = [r for r in source if r['quarter'] == q and r['geography'] != 'England and Wales']
        assert len(regions) == 7
        n = int(national['transactions_recorded'])
        mapped = sum(int(r['transactions_recorded']) for r in regions)
        assert n == int(coverage[q]['national_transactions'])
        assert mapped == int(coverage[q]['mapped_transactions'])
        m = float(national['median_price_gbp'])
        equal = mean(float(r['median_price_gbp']) for r in regions)
        weighted = sum(float(r['median_price_gbp']) * int(r['transactions_recorded']) for r in regions) / mapped
        results.append(dict(quarter=q, national_transactions=n, mapped_transactions=mapped,
            unmapped_transactions=n-mapped, source_national_median_gbp=m,
            equal_mean_of_regional_medians_gbp=equal,
            count_weighted_mean_of_regional_medians_gbp=weighted,
            equal_minus_source_gbp=equal-m, weighted_minus_source_gbp=weighted-m,
            weighted_difference_pct=100*(weighted/m-1)))
    return source, results


def synthetic_examples():
    pairs = {'A': ([100000, 200000, 210000], [220000, 300000, 400000]),
             'B': ([100000, 200000, 290000], [280000, 300000, 400000])}
    rows = []
    for name, (a,b) in pairs.items():
        assert len(a) == len(b) == 3 and median(a) == 200000 and median(b) == 300000
        rows.append(dict(synthetic_scenario=name, region_1_prices_gbp=';'.join(map(str,a)),
            region_2_prices_gbp=';'.join(map(str,b)), region_1_median_gbp=median(a),
            region_2_median_gbp=median(b), observations_per_region=3,
            weighted_mean_of_medians_gbp=250000, pooled_median_gbp=median(a+b)))
    assert rows[0]['pooled_median_gbp'] == 215000 and rows[1]['pooled_median_gbp'] == 285000
    return rows


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', default='reproduced')
    args = parser.parse_args(); root = Path(__file__).resolve().parent
    source, results = calculate(root)
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    write_csv(out/'median_shortcuts.csv', results)
    write_csv(out/'q3_regional_inputs.csv', [r for r in source if r['quarter'] == '2026-Q3' and r['geography'] != 'England and Wales'])
    write_csv(out/'synthetic_counterexample.csv', synthetic_examples())
    print('Verified 15 quarter reconciliations and two synthetic examples. Three CSVs written.')
