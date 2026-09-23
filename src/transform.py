"""Data Transformation and Filtering Module for Philippine Customs Data.

Author: Gab (Work B)
Description: Handles filtering via .loc, sorting, and adding derived columns.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np


def filter_and_transform_data(
    df: pd.DataFrame, 
    config: Dict[str, Any], 
    duty_rate: float = 0.05
) -> Tuple[pd.DataFrame, int]:
    col1 = config["FILTER_COL_1"]
    val1 = config["FILTER_VAL_1"]
    col2 = config["FILTER_COL_2"]
    val2 = config["FILTER_VAL_2"]

    rows_before = len(df)

    # 1. Dual-condition filtering using .loc
    mask = (df[col1] == val1) & (df[col2] > val2)
    filtered_df = df.loc[mask].copy()

    if len(filtered_df) == 0:
        raise ValueError("Filter returned 0 rows.")

    return filtered_df, rows_before - len(filtered_df)
