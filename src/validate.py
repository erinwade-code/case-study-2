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

def check_raw_equals_selected_plus_excluded(
    raw_df: pd.DataFrame,
    selected_df: pd.DataFrame,
    excluded_df: pd.DataFrame
) -> dict[str, Any]:
    """Raw rows must equal selected rows plus excluded rows exactly."""
    return run_check(
        "raw_equals_selected_plus_excluded",
        expected=len(raw_df),
        actual=len(selected_df) + len(excluded_df),
        tolerance=0
    )

def check_grouped_row_counts(
    selected_df: pd.DataFrame,
    grouped_df: pd.DataFrame
) -> dict[str, Any]:
    """Grouped row counts must sum to the selected row count."""
    return run_check(
        "grouped_row_counts_sum_to_selected",
        expected=len(selected_df),
        actual=grouped_df["row_count"].sum(),
        tolerance=0
    )

def check_grouped_sum_matches_independent_sum(
    selected_df: pd.DataFrame,
    grouped_df: pd.DataFrame,
    measure_col: str = "dutiablevaluephp"
) -> dict[str, Any]:
    """
    Grouped sums must equal a sum computed directly from the selected
    data, independent of the groupby operation.
    """
    independent_sum = selected_df[measure_col].sum()
    grouped_sum = grouped_df["sum"].sum()
    return run_check(
        "grouped_sum_matches_independent_sum",
        expected=independent_sum,
        actual=grouped_sum,
        tolerance=ABSOLUTE_TOLERANCE
    )

def check_pivot_interior_sum(
    selected_df: pd.DataFrame,
    pivot_df: pd.DataFrame,
    measure_col: str = "dutiablevaluephp"
) -> dict[str, Any]:
    """
    The pivot table's interior (excluding margins) must sum to the
    same independent total. Margins are excluded to avoid double-counting.
    """
    independent_sum = selected_df[measure_col].sum()
    interior = pivot_df.drop(index="All", errors="ignore").drop(columns="All", errors="ignore")
    return run_check(
        "pivot_interior_sum_matches_independent_sum",
        expected=independent_sum,
        actual=interior.to_numpy().sum(),
        tolerance=ABSOLUTE_TOLERANCE
    )

def check_loop_vs_vectorized(loop_result: float, vectorized_result: float) -> dict[str, Any]:
    """Loop and vectorized NumPy calculations must agree."""
    return run_check(
        "loop_and_vectorized_agree",
        expected=loop_result,
        actual=vectorized_result,
        tolerance=ABSOLUTE_TOLERANCE
    )