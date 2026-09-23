import pandas as pd

CAT_COL_1 = "countryorigin_iso3"
CAT_COL_2 = "tq"
MEASURE_COL = "dutiablevaluephp"

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

def pivot_with_margins(
    df: pd.DataFrame,
    index: str = "port",
    columns: str = "tm",
    values: str = "dutiestaxes",
) -> pd.DataFrame:
    """
    Build a pivot table with row/column totals (margins=True).
    Expects df to already be aggregated at (index, columns) level
    -- i.e. call this on the output of group_by_two-style data,
    so pivoting large raw data isn't required.
    """
    pivot = pd.pivot_table(
        df,
        index=index,
        columns=columns,
        values=values,
        aggfunc="sum",
        margins=True,
        margins_name="Total",
        fill_value=0,
    )
    return pivot

def top10(grouped_df: pd.DataFrame, value_col: str = "dutiestaxes") -> pd.DataFrame:
    """Return the top 10 rows of an already-grouped DataFrame by value_col."""
    return grouped_df.sort_values(value_col, ascending=False).head(10)

def duty_rate_summary(port_sums: dict) -> pd.DataFrame:
    """
    Compute effective duty rate (dutiestaxes / dutiablevaluephp) per port.
 
    port_sums: dict like
        {
          "Port of Manila": {"dutiestaxes": 123.0, "dutiablevaluephp": 456.0},
          ...
        }
    """
    rows = []
    for port, sums in port_sums.items():
        taxes = sums.get("dutiestaxes", 0)
        value = sums.get("dutiablevaluephp", 0)
        rate = (taxes / value) if value else 0
        rows.append({"port": port, "dutiestaxes": taxes,
                      "dutiablevaluephp": value, "effective_duty_rate": rate})
    return pd.DataFrame(rows).sort_values("effective_duty_rate", ascending=False)
 
