# Generates validation.csv and audit_log.csv
# exits nonzero on failure

#modules import
import sys
import pandas as pd 
from typing import Any

REFERENCE_ROW_COUNT: int = 2_236_612
REFERENCE_COLUMN_COUNT: int = 30
REFERENCE_DUTIABLE_SUM: float = 3_587_267_375_257.0
ABSOLUTE_TOLERANCE: float = 1.00   # PHP
RELATIVE_TOLERANCE: float = 0.0

def run_check(
    check_name: str,
    expected: float,
    actual: float,
    tolerance: float = ABSOLUTE_TOLERANCE
) -> dict[str, Any]:

    discrepancy = abs(expected - actual)
    passed = discrepancy <= tolerance
    return {
        "check": check_name,
        "expected": expected,
        "actual": actual,
        "tolerance": tolerance,
        "pass": passed,
    }

def check_reference_totals(raw_df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Compare the raw loaded data against the instructor's supplied
    reference totals for Customs 2015 (row count and dutiable value sum).
    """
    results = []
    results.append(run_check(
        "raw_row_count_matches_reference",
        expected=REFERENCE_ROW_COUNT,
        actual=len(raw_df),
        tolerance=0  # row counts must match exactly
    ))
    results.append(run_check(
        "raw_dutiable_sum_matches_reference",
        expected=REFERENCE_DUTIABLE_SUM,
        actual=raw_df["dutiablevaluephp"].sum(),
        tolerance=ABSOLUTE_TOLERANCE
    ))
    return results