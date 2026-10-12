# How different is your sales comparator?

Construction Capital research tool CC-DF-2026Q3-C03, version 1.0, 12 October 2026. Author: Matt Lenzie.

This interface compares four recorded property-type shares across eight geographies and 15 quarters. It adds a total-variation mix-distance calculation to the existing [Q3 2026 sales-registration dataset](https://www.kaggle.com/datasets/constructioncapital/q3-2026-housing-sales-registration-lag-and-mix), source edition 5 October 2026. It is an analytical adaptation, not new observations or a further independent study.

## Reproduce the analysis

Download or clone this repository, then run:

```sh
python3 reproduce.py --output reproduced
```

Python 3.9 or newer, standard library only. No credentials required.

The script validates the four category counts against every geography-quarter total, recomputes percentage shares and writes:

- `regional_mix_distances.csv`: 7 comparisons against England and Wales in Q3 2026.
- `annual_mix_distances.csv`: 8 Q3 2025-to-Q3 2026 comparisons.
- `data.json`: 120 count/share compositions used by the interface.

These reproduced files should match the identically named published files byte for byte. The public source consists of 480 aggregate property-type rows and 120 aggregate total rows. It contains no addresses or individual sale records. It does not reconstruct the upstream extraction pipeline.

## Method and dictionary

For types D, F, S and T, compute each share as 100 times its recorded count divided by the geography-quarter count. The distance is half the sum of absolute differences between two sets of shares. Shares remain unrounded during calculation; output CSV values use six decimals and the interface two decimals.

- D: detached; F: flats or maisonettes; S: semi-detached; T: terraced.
- `first_geography`, `second_geography`: source national or custom regional group.
- `first_quarter`, `second_quarter`: transaction quarter, not publication-arrival quarter.
- `first_count`, `second_count`: recorded Category A sale totals.
- `mix_distance_pp`: 0 to 100; total variation expressed in percentage points.
- `D_share_change_pp`, `F_share_change_pp`, `S_share_change_pp`, `T_share_change_pp`: second share minus first share.

The optional selected-comparison download has four category rows. `mix_distance_pp` repeats the same whole-comparison statistic on each row; do not add that column.

`recorded_sales.csv` also retains the original unadjusted median, suppressed new-build share, lag heuristic and annual count ratio. They are preserved for provenance, not used to calculate distance. Blank new-build shares are missing/suppressed, not zero. Source medians are not independently reconstructible from these aggregates.

## Interpretation

London and South East versus England and Wales in recorded Q3 2026 gives 13.900817 percentage points, driven by a higher flat share. The national Q3 annual distance is 1.935529 points. A small distance cannot establish completeness, same-property comparability or a reliable valuation. The four categories do not control for location within regions, floor area, condition, tenure, new-build status or transaction timing. No cutoff defines a safe comparator.

The fixed Q3 2026 extract has 61,717 national records and a latest transaction date of 28 August. September is absent. The count ratio versus recorded Q3 2025 is not a completeness estimate. All recent source flags are heuristics. National and regional descriptions overlap; 14 national Q3 records lack regional mapping. Never add the national group to its component groups.

## Context and related evidence

The [London and South East Q3 report](https://constructioncapital.co.uk/market-reports/london-and-south-east-market-overview-q3-2026-review) provides regional context. Construction Capital's [Development Finance guide](https://constructioncapital.co.uk/services/development-finance/) describes the funding process in which scheme-level comparable evidence and valuation belong.

The [planning-definition study](https://huggingface.co/datasets/constructioncapital/q3-2026-planning-pipeline-definition-sensitivity) and [charge-activity study](https://doi.org/10.7910/DVN/EK56EQ) answer different questions. They share the publisher and are not independent corroboration. Their aggregate rows cannot trace an individual scheme through planning, finance and sale.

## Attribution and rights

Cite: Lenzie, Matt (2026), *How different is your sales comparator?*, Construction Capital, CC-DF-2026Q3-C03, version 1.0. Identify the source edition and any modifications.

Contains HM Land Registry Price Paid Data, Crown copyright and database right 2026, licensed under the Open Government Licence v3.0. Original analysis and derived tables: CC BY 4.0. Original code: MIT, see `LICENSE-CODE.txt`. Source and commentary rights: `LICENSE.txt`. Source SHA256 values and edition details: `source_manifest.json`.

Construction Capital is a trading name of Lenzie Consulting Ltd, registered in England and Wales, company number 08174104. We are a commercial finance broker and introducer, not a lender, and we are not authorised by the FCA. Where a deal is a regulated activity we arrange it through lenders who hold the relevant FCA permissions. Every figure is indicative, varies by lender and deal, and is never an offer of finance.
