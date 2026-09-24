# FINAL COMMIT 


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

    # 2. Sort records by numerical measure (descending)
    measure = config["NUMERICAL_MEASURE"]
    filtered_df.sort_values(by=measure, ascending=False, inplace=True)

    # 3. Derived Column 1 (Numeric): Estimated Duty in PHP
    filtered_df["estimated_duty_php"] = filtered_df[measure] * duty_rate

    # 4. Derived Column 2 (Category/Flag): High vs. Low Value
    median_val = filtered_df[measure].median()
    filtered_df["value_category_flag"] = np.where(
        filtered_df[measure] >= median_val, "High_Value", "Low_Value"
    )

    rows_after = len(filtered_df)
    excluded_rows = rows_before - rows_after

    return filtered_df, excluded_rows
# --- Local Standalone Unit Test ---
if __name__ == "__main__":
    print("Testing Work B transformation logic...")
    mock_data = pd.DataFrame({
        "countryorigin_iso3": ["CHN", "USA", "CHN", "CHN"],
        "q": [10, 5, 0, 25],
        "dutiablevaluephp": [100000.0, 50000.0, 20000.0, 300000.0]
    })
    
    mock_config = {
        "FILTER_COL_1": "countryorigin_iso3",
        "FILTER_VAL_1": "CHN",
        "FILTER_COL_2": "q",
        "FILTER_VAL_2": 0,
        "NUMERICAL_MEASURE": "dutiablevaluephp"
    }

    filtered_res, excluded_count = filter_and_transform_data(mock_data, mock_config)
    print(f"Excluded rows count: {excluded_count}")
