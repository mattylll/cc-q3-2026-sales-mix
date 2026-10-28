"""Controlled failure examples; original inputs remain untouched."""
import copy
import unittest
from pathlib import Path
from aggregation_guard import audit_release, load_csv, sum_compatible, NATIONAL

class AggregationChecks(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).parent
        self.sales = load_csv(root / "recorded_sales.csv")
        self.coverage = load_csv(root / "regional_mapping_coverage.csv")
        self.q3 = [r for r in self.sales if r["quarter"] == "2026-Q3"]

    def test_valid_release_and_known_q3(self):
        result = audit_release(self.sales, self.coverage)
        self.assertEqual(len(result), 15)
        self.assertEqual((result[-1]["national_records"], result[-1]["mapped_regional_records"], result[-1]["unmapped_records"]), (61717,61703,14))

    def test_national_selection(self):
        self.assertEqual(sum_compatible([r for r in self.q3 if r["geography"] == NATIONAL]),61717)

    def test_regional_selection(self):
        self.assertEqual(sum_compatible([r for r in self.q3 if r["geography"] != NATIONAL]),61703)

    def test_reject_mixed_levels(self):
        with self.assertRaisesRegex(ValueError, "Mixed national"):
            sum_compatible(self.q3)

    def test_reject_duplicate_key(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            sum_compatible([self.q3[0],self.q3[0]])

    def test_reject_mixed_quarters(self):
        with self.assertRaisesRegex(ValueError, "Mixed quarters"):
            sum_compatible([r for r in self.sales if r["geography"] == NATIONAL])

    def test_reject_missing_region(self):
        with self.assertRaisesRegex(ValueError, "Release keys"):
            audit_release(self.sales[:-1], self.coverage)

    def test_reject_unexplained_gap(self):
        changed=copy.deepcopy(self.coverage); changed[-1]["unmapped_transactions"]="0"
        with self.assertRaisesRegex(ValueError, "do not reconcile"):
            audit_release(self.sales, changed)

    def test_reject_unknown_geography(self):
        changed=copy.deepcopy(self.q3[:1]); changed[0]["geography"]="London"
        with self.assertRaisesRegex(ValueError,"Undeclared"):
            sum_compatible(changed)

    def test_reject_invalid_count(self):
        for value in ["-1","2.5","", "True"]:
            with self.subTest(value=value):
                changed=copy.deepcopy(self.q3[:1]);changed[0]["transactions_recorded"]=value
                with self.assertRaisesRegex(ValueError,"integer"):
                    sum_compatible(changed)

    def test_reject_empty_selection(self):
        with self.assertRaisesRegex(ValueError,"Empty"):
            sum_compatible([])

if __name__ == "__main__":
    unittest.main()
