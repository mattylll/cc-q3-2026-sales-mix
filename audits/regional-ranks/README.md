# Same regional order, different development exit assumptions

CC-DF-2026Q3-A05 | Matt Lenzie / Construction Capital | Prepared 2 November 2026.

This is a supporting analytical adaptation of CC-DF-2026Q3-03, not a new independent study or dataset. It adds a seven-group rank comparison, changes in endpoint spread, and differences from the retained national median. It does not estimate a final Q3 market result or a scheme valuation.

The frozen aggregate source was published on 5 October 2026. Latest transaction: 28 August 2026; September is absent and registration lag remains. Seven custom regions cover England and Wales, not the whole UK. Category A records. Source medians are retained statistics, not recalculated from transaction-level records.

## Reproduce

```sh
python3 reproduce.py --output reproduced
```

Standard library only. Optional `--chart` requires matplotlib. It creates a PNG in addition to the calculated CSVs and summary.

- `recorded_sales.csv`: 120 original aggregate source rows, unchanged.
- `derived/selected_source_rows.csv`: 16 selected national/regional observations for Q3 2025 and Q3 2026.
- `derived/regional_rank_comparison.csv`: 7 derived regional comparisons.
- `derived/summary.json`: reproducible headline results and input hash.
- `derived/regional-ranks.png`: original chart.
- `parent_source_manifest.json`: provenance of the public aggregate source.
- `LICENSE.txt`: separate original content, code and underlying data rights.

Rank 1 is the highest median within the seven reporting groups. Rank change is previous rank minus current rank. GBP differences subtract 2025 from 2026. Percentage changes divide the difference by the 2025 value. Differences from national subtract the retained England and Wales median for 2026-Q3; corresponding percentages divide by that national median. No counts or regional medians are averaged to reconstruct the national median.

Seven unchanged ranks do not imply stable values or sample representativeness. The £225,000 endpoint spread is between regional group medians, not a range of individual house prices, development margins or valuation bounds. National recorded transactions include 14 Q3 2026 records without regional mapping.

Parent dataset: https://www.kaggle.com/datasets/constructioncapital/q3-2026-housing-sales-registration-lag-and-mix

Source context: https://constructioncapital.co.uk/market-reports/london-and-south-east-market-overview-q3-2026-review

Finance process: https://constructioncapital.co.uk/services/development-finance/

Construction Capital is a property-finance brokerage. Hosting and reuse do not imply independent endorsement or peer review.
