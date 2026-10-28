"""Release-specific aggregation guard, Python standard library, no network calls.

Copyright 2026 Matt Lenzie / Construction Capital. MIT licence; see LICENSE.txt.
The declared regional groups are disjoint in this publisher's fixed source mapping.
This module cannot infer geographic disjointness from names or certify completeness.
"""
import csv
import json
from pathlib import Path
from collections import Counter

NATIONAL = "England and Wales"
REGIONS = {"East of England", "London & South East", "Midlands",
           "North East & Yorkshire", "North West", "South West", "Wales"}
QUARTERS = {f"{y}-Q{q}" for y in range(2023, 2027)
            for q in range(1, 5) if (y, q) <= (2026, 3)}

def count(value):
    s = str(value)
    if not s.isascii() or not s.isdigit():
        raise ValueError("Count must be a non-negative integer")
    return int(s)

def load_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def scope(geography):
    if geography == NATIONAL:
        return "national"
    if geography in REGIONS:
        return "regional"
    raise ValueError("Undeclared geography")

def sum_compatible(rows):
    """Require one quarter and one declared geographical level before summing."""
    if not rows:
        raise ValueError("Empty selection")
    if len({r["quarter"] for r in rows}) != 1:
        raise ValueError("Mixed quarters")
    if len({scope(r["geography"]) for r in rows}) != 1:
        raise ValueError("Mixed national and regional levels")
    keys = [(r["quarter"], r["geography"]) for r in rows]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate quarter/geography key")
    return sum(count(r["transactions_recorded"]) for r in rows)

def audit_release(sales, coverage):
    expected = {(q, g) for q in QUARTERS for g in REGIONS | {NATIONAL}}
    keys = [(r["quarter"], r["geography"]) for r in sales]
    if set(keys) != expected or any(n != 1 for n in Counter(keys).values()):
        raise ValueError("Release keys differ from the declared 15 x 8 panel")
    ck = [r["quarter"] for r in coverage]
    if set(ck) != QUARTERS or len(ck) != len(QUARTERS):
        raise ValueError("Coverage keys differ from declared quarters")
    cv = {r["quarter"]: r for r in coverage}
    results = []
    for q in sorted(QUARTERS):
        rows = [r for r in sales if r["quarter"] == q]
        n = sum_compatible([r for r in rows if r["geography"] == NATIONAL])
        m = sum_compatible([r for r in rows if r["geography"] in REGIONS])
        u = count(cv[q]["unmapped_transactions"])
        if n != count(cv[q]["national_transactions"]) or m != count(cv[q]["mapped_transactions"]) or n != m + u:
            raise ValueError("National, mapped and unmapped counts do not reconcile")
        results.append({"quarter": q, "national_records": n,
                        "mapped_regional_records": m, "unmapped_records": u,
                        "unsafe_sum_of_all_rows": n + m,
                        "overstatement_records": m,
                        "overstatement_pct": round(100 * m / n, 6) if n else None})
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path(__file__).parent)
    parser.add_argument("--output", type=Path, default=Path("reproduced"))
    args = parser.parse_args()
    rows = audit_release(load_csv(args.source / "recorded_sales.csv"),
                         load_csv(args.source / "regional_mapping_coverage.csv"))
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "aggregation_audit.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(json.dumps({"quarters_reconciled": len(rows), "q3_2026": rows[-1],
                      "scope": "Aggregation semantics and internal reconciliation only; not completeness or source accuracy."}, indent=2))

if __name__ == "__main__":
    main()
