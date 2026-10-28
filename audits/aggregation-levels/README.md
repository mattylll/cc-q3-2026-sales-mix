# Aggregation levels in the Q3 2026 housing sales release

Supporting methods adaptation CC-DF-2026Q3-A03. Matt Lenzie / Construction Capital, 28 October 2026. This is a deterministic consumer-side guard and audit, not a new independent study.

The unchanged inputs are from CC-DF-2026Q3-03, version 1.0, frozen 5 October 2026. Latest transaction date 28 August; September absent. Source: https://www.kaggle.com/datasets/constructioncapital/q3-2026-housing-sales-registration-lag-and-mix

Run `python3 aggregation_guard.py --output reproduced` and `python3 -m unittest -v test_guard.py` from this directory. Python3 standard library only; no network, credentials or original private repository required. The script validates the 15-quarter by 8-geography declared panel and writes aggregation_audit.csv. Review the explicit geography mapping before adapting the guard to another dataset.

The unsafe total is a demonstrated invalid operation, not a reported source statistic or discovered HM Land Registry error. It adds a national benchmark to its mapped regional components. The legitimate reconciliation adds the mapped regions and the separately declared unmapped residual.

The checks do not establish complete Q3 coverage, row-level accuracy, scheme valuations or causal market trends. Source medians are not additive. Retain LICENSE.txt, source_manifest.json and source-input-hashes.json when reusing this package.
