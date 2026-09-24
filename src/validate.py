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
    dutiable_sum = raw_df["sum"].sum() if "sum" in raw_df.columns else raw_df["dutiablevaluephp"].sum()
    results.append(run_check(
        "raw_dutiable_sum_matches_reference",
        expected=REFERENCE_DUTIABLE_SUM,
        actual=dutiable_sum,
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
    if measure_col in selected_df.columns:
        independent_sum = float(selected_df[measure_col].sum())
    elif "sum" in selected_df.columns:
        independent_sum = float(selected_df["sum"].sum())
    else:
        independent_sum = 0.0

    interior = pivot_df.drop(index=["Total", "All"], errors="ignore").drop(columns=["Total", "All"], errors="ignore")
    
    numeric_interior = interior.select_dtypes(include=["number"])

    return run_check(
        "pivot_interior_sum_matches_independent_sum",
        expected=independent_sum,
        actual=float(numeric_interior.to_numpy().sum()),
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

def build_validation_table(all_checks: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(all_checks)


def save_validation_csv(validation_df: pd.DataFrame, output_folder: str) -> None:
    validation_df.to_csv(f"{output_folder}/validation.csv", index=False)



class AuditLog:
    """
    Tracks pipeline operations for audit_log.csv.

    Each entry records what step ran, what operation happened, what rule
    it enforced, and how many rows existed before/after.
    """

    def __init__(self) -> None:
        """Initialize an empty audit log."""
        self.entries: list[dict[str, Any]] = []

    def record(
        self,
        step: str,
        operation: str,
        rule: str,
        rows_before: int,
        rows_after: int
    ) -> None:
        """Add one entry to the audit log."""
        self.entries.append({
            "step": step,
            "operation": operation,
            "rule": rule,
            "rows_before": rows_before,
            "rows_after": rows_after,
        })

    def to_dataframe(self) -> pd.DataFrame:
        """Return all entries as a DataFrame."""
        return pd.DataFrame(self.entries)

    def save(self, output_folder: str) -> None:
        """Write audit_log.csv to the configured output folder."""
        self.to_dataframe().to_csv(f"{output_folder}/audit_log.csv", index=False)


def run_all_validations(
    raw_df: pd.DataFrame,
    selected_df: pd.DataFrame,
    excluded_df: pd.DataFrame,
    grouped_df: pd.DataFrame,
    pivot_df: pd.DataFrame,
    loop_result: float,
    vectorized_result: float,
    output_folder: str
) -> bool:
    """
    Run every required check, save validation.csv, and return whether
    all checks passed.
    """
    all_checks = []
    all_checks += check_reference_totals(raw_df)
    all_checks.append(check_raw_equals_selected_plus_excluded(raw_df, selected_df, excluded_df))
    all_checks.append(check_grouped_row_counts(selected_df, grouped_df))
    all_checks.append(check_grouped_sum_matches_independent_sum(selected_df, grouped_df))
    all_checks.append(check_pivot_interior_sum(selected_df, pivot_df))
    all_checks.append(check_loop_vs_vectorized(loop_result, vectorized_result))

    validation_df = build_validation_table(all_checks)
    save_validation_csv(validation_df, output_folder)

    all_passed = validation_df["pass"].all()

    if not all_passed:
        failed = validation_df[~validation_df["pass"]]
        print("VALIDATION FAILED. Discrepancies found:")
        print(failed.to_string(index=False))

    return all_passed