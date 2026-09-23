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