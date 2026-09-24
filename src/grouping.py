# FINAL COMMIT 

import pandas as pd

CAT_COL_1 = "countryorigin_iso3"
CAT_COL_2 = "tq"
MEASURE_COL = "dutiablevaluephp"

def group_by_single(df: pd.DataFrame, group_col: str = CAT_COL_1,
                     measure_col: str = MEASURE_COL) -> pd.DataFrame:
    """Group by one category column; report count, valid count, sum, mean."""
    result = df.groupby(group_col, dropna=False).agg(
        row_count=(measure_col, "size"),
        valid_count=(measure_col, "count"),   # excludes NaN
        sum=(measure_col, "sum"),
        mean=(measure_col, "mean"),
    ).reset_index()
    return result.sort_values("sum", ascending=False)

def group_by_two(df: pd.DataFrame,
                  group_cols=(CAT_COL_1, CAT_COL_2),
                  measure_col: str = MEASURE_COL) -> pd.DataFrame:
    """Group by both category columns; report row count and measure sum."""
    result = df.groupby(list(group_cols), dropna=False).agg(
        row_count=(measure_col, "size"),
        sum=(measure_col, "sum"),
    ).reset_index()
    return result.sort_values("sum", ascending=False)

def pivot_with_margins(df: pd.DataFrame,
                        index: str = CAT_COL_1,
                        columns: str = CAT_COL_2,
                        values: str = "sum") -> pd.DataFrame:
    """
    Build a pivot table with row/column totals (margins=True).
    Expects df already aggregated at (index, columns) level, i.e. the
    output of group_by_two, so re-scanning raw data isn't required.
    """
    pivot = pd.pivot_table(
        df, index=index, columns=columns, values=values,
        aggfunc="sum", margins=True, margins_name="Total", fill_value=0,
    )
    return pivot

def top10(grouped_df: pd.DataFrame, sum_col: str = "sum") -> pd.DataFrame:
    """Return up to the top 10 rows of grouped_df sorted by sum_col."""
    return grouped_df.sort_values(sum_col, ascending=False).head(10)

def missing_value_report(counts: dict, default_measure: str = MEASURE_COL) -> pd.DataFrame:
    """
    Report how many rows had a missing measure value per group.
 
    counts: dict like
        {"CHN": {"row_count": 500, "valid_count": 498}, ...}
    default_measure: label only, used in the output column name so the
    report is self-describing (parameter has a default value).
    """
    rows = []
    for group, c in counts.items():
        row_count = c.get("row_count", 0)
        valid_count = c.get("valid_count", 0)
        missing = row_count - valid_count
        rows.append({
            "group": group,
            "row_count": row_count,
            "valid_count": valid_count,
            f"missing_{default_measure}": missing,
        })
    return pd.DataFrame(rows).sort_values(f"missing_{default_measure}", ascending=False)
 
