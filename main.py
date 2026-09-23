import os
import sys
import pandas as pd

import transform

CHUNKSIZE = 200_000
REQUIRED_COLUMNS = {transform.CAT_COL_1, transform.CAT_COL_2, transform.MEASURE_COL}
 
 
def validate_input(path: str) -> None:
    """Conditions to handle invalid input."""
    if not path:
        raise ValueError("No input file path given.")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")
    if not path.lower().endswith(".csv"):
        raise ValueError(f"Expected a .csv file, got: {path}")
 
    # Peek at the header only, to fail fast before processing 2M+ rows
    header = pd.read_csv(path, nrows=0, encoding="latin1")
    missing = REQUIRED_COLUMNS - set(header.columns)
    if missing:
        raise ValueError(f"Input file is missing required columns: {missing}")
 
 
def process_in_chunks(path: str):
    """
    Loop to process records/chunks/outputs.
    Reads the (large) CSV in chunks, applies extract/clean (placeholders
    for now), and accumulates partial aggregates per chunk so the full
    2.2M-row file is never held in memory at once.
    """
    single_partials = []   # per-chunk group_by_single results
    two_partials = []      # per-chunk group_by_two results
    missing_counts: dict[str, dict[str, int]] = {}  # for the standalone function
 
    reader = pd.read_csv(
        path, chunksize=CHUNKSIZE, encoding="latin1", low_memory=False
    )
 
    for i, chunk in enumerate(reader, start=1):
        # --- Work A / Work B would slot in here ---
        # chunk = clean.clean_chunk(chunk)
 
        single_partials.append(transform.group_by_single(chunk))
        two_partials.append(transform.group_by_two(chunk))
 
        # Running row_count / valid_count per country, for missing_value_report
        chunk_counts = chunk.groupby(transform.CAT_COL_1)[transform.MEASURE_COL].agg(
            row_count="size", valid_count="count"
        )
        for country, row in chunk_counts.iterrows():
            entry = missing_counts.setdefault(country, {"row_count": 0, "valid_count": 0})
            entry["row_count"] += int(row["row_count"])
            entry["valid_count"] += int(row["valid_count"])
 
        print(f"  processed chunk {i} ({len(chunk):,} rows)")
 
    return single_partials, two_partials, missing_counts
 

def combine_single(partials: list[pd.DataFrame]) -> pd.DataFrame:
    """Re-aggregate per-chunk group_by_single results into final totals."""
    combined = pd.concat(partials, ignore_index=True)
    result = combined.groupby(transform.CAT_COL_1, dropna=False).agg(
        row_count=("row_count", "sum"),
        valid_count=("valid_count", "sum"),
        sum=("sum", "sum"),
    ).reset_index()
    result["mean"] = result["sum"] / result["valid_count"]
    return result.sort_values("sum", ascending=False)
 
 
def combine_two(partials: list[pd.DataFrame]) -> pd.DataFrame:
    """Re-aggregate per-chunk group_by_two results into final totals."""
    combined = pd.concat(partials, ignore_index=True)
    result = combined.groupby(
        [transform.CAT_COL_1, transform.CAT_COL_2], dropna=False
    ).agg(
        row_count=("row_count", "sum"),
        sum=("sum", "sum"),
    ).reset_index()
    return result.sort_values("sum", ascending=False)
 
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "2015.csv"
 
    print(f"Validating input: {path}")
    validate_input(path)
 
    print("Processing file in chunks...")
    single_partials, two_partials, port_sums = process_in_chunks(path)
 
    # Re-aggregate the partial (per-chunk) sums into final totals
    print("Combining chunk results...")
    grouped = transform.group_by_single(pd.concat(single_partials, ignore_index=True))
    grouped_two = transform.group_by_two(
        pd.concat(two_partials, ignore_index=True),
        group_cols=("countryorigin_iso3", "tm"),
    )
    pivot = transform.pivot_with_margins(
        grouped_two, index="countryorigin_iso3", columns="tm", values="dutiestaxes"
    )
    top_10 = transform.top10(grouped)

    duty_rates = transform.duty_rate_summary(port_sums)


    grouped.to_csv("grouped.csv", index=False)
    grouped_two.to_csv("grouped_two.csv", index=False)
    pivot.to_csv("pivot.csv")
    top_10.to_csv("top10.csv", index=False)
    duty_rates.to_csv("duty_rate_summary.csv", index=False)
 
    print("Done. Wrote: grouped.csv, grouped_two.csv, pivot.csv, top10.csv, duty_rate_summary.csv")
 
 
if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
