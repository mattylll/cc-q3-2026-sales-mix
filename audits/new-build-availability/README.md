# New-build field availability audit

**CC-DF-2026Q3-A02 | 13 October 2026 | Matt Lenzie, Construction Capital**

Supporting diagnostic of the existing [Q3 sales dataset on Kaggle](https://www.kaggle.com/datasets/constructioncapital/q3-2026-housing-sales-registration-lag-and-mix), version 1.0, frozen 5 October 2026. Not a new observational dataset or an independent study.

Download `recorded_sales.csv` from that public dataset. Then run:

```sh
python3 reproduce.py /path/to/recorded_sales.csv --output reproduced
```

The standard-library script counts empty new-build-share cells and the exact True/False source lag strings separately. It checks unique geography-quarter keys and value ranges, without filling missing values. `audit-summary.json` includes the source SHA-256. `field-availability-by-quarter.csv` has 15 derived rows: quarter; row count; share-present count; share-withheld count; lag-true count; withheld-and-lag-false count. All count fields are counts of geography-quarter rows.

## Findings

120 rows span 15 quarters and 8 geographies. New-build share is present in 80 rows and withheld in 40. The cross-tabulation is 80 present/lag-false, 16 withheld/lag-false and 24 withheld/lag-true. There are no present/lag-true rows. The 16 withheld/lag-false rows are Q3 and Q4 2025. National and regional rows overlap; these are not independent observations or counts of missing transactions. False is a heuristic flag, not certification of complete data.

Recent Q3 2026 sales are provisional: latest transaction date 28 August; September absent in the frozen extract. No imputation, nowcast or scheme valuation is supplied. Source blanks are withheld values, never zero.

For regional interpretation see the [London and South East Q3 review](https://constructioncapital.co.uk/market-reports/london-and-south-east-market-overview-q3-2026-review). Construction Capital's [Development Finance overview](https://constructioncapital.co.uk/services/development-finance/) provides commercial service context. All are the publisher's resources, not independent endorsements.

## Rights

Original analysis and derived presentation: copyright 2026 Matt Lenzie / Construction Capital, CC BY 4.0. Original code: MIT, under the repository's existing licence notice. Contains HM Land Registry Price Paid Data, Crown copyright and database right 2026, under OGL v3.0. See the parent LICENSE-CODE.txt and LICENSE.txt and the Kaggle source package for attribution and source scope. No private entities or transaction-level records are included.
