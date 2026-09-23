import pandas as pd

def group_by_single(df: pd.DataFrame, group_col: str = "countryorigin_iso3") -> pd.DataFrame:
    """
    Group by one column and sum the key value columns.
    Works on a full DataFrame OR on a partial-sum DataFrame (chunk results),
    since summing already-summed rows again is still correct.
    """

    result = (
        df.groupby(group_col, dropna=False)[["dutiestaxes", "dutiablevaluephp"]]
        .sum()
        .reset_index()
        .sort_values("dutiestaxes", ascending=False)
    )
    return result

def group_by_two(
    df: pd.DataFrame,
    group_cols=("countryorigin_iso3", "port"),
) -> pd.DataFrame:
    """Group by two columns and sum dutiestaxes."""
    result = (
        df.groupby(list(group_cols), dropna=False)["dutiestaxes"]
        .sum()
        .reset_index()
        .sort_values("dutiestaxes", ascending=False)
    )
    return result
