import os
import sys
import pandas as pd

from config import config
from src.loader import Loader
from src import grouping, plots, validate, transform, numpy_ops

CHUNKSIZE = 200_000
REQUIRED_COLUMNS = {grouping.CAT_COL_1, grouping.CAT_COL_2, grouping.MEASURE_COL}
 
 
def validate_input(path: str) -> None:
    """Conditions to handle invalid input."""
    if not path:
        raise ValueError("No input file path given.")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")
    if not path.lower().endswith(".csv"):
        raise ValueError(f"Expected a .csv file, got: {path}")
 
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
    single_partials = [] 
    two_partials = [] 
    missing_counts: dict[str, dict[str, int]] = {}  
 
    reader = pd.read_csv(
        path, chunksize=CHUNKSIZE, encoding="latin1", low_memory=False
    )
 
    for i, chunk in enumerate(reader, start=1):
 
        single_partials.append(grouping.group_by_single(chunk))
        two_partials.append(grouping.group_by_two(chunk))
 
        chunk_counts = chunk.groupby(grouping.CAT_COL_1)[grouping.MEASURE_COL].agg(
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
    result = combined.groupby(grouping.CAT_COL_1, dropna=False).agg(
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
        [grouping.CAT_COL_1, grouping.CAT_COL_2], dropna=False
    ).agg(
        row_count=("row_count", "sum"),
        sum=("sum", "sum"),
    ).reset_index()
    return result.sort_values("sum", ascending=False)
 
def main():
    print("Loading raw dataset for reference validation...")
    loader = Loader(config)
    raw_df = loader.load()  
    path = sys.argv[1] if len(sys.argv) > 1 else config["input_path"]
 
    print(f"Validating input: {path}")
    validate_input(path)
 
    print("Processing file in chunks...")
    single_partials, two_partials, missing_counts = process_in_chunks(path)
 
    print("Combining chunk results...")
    grouped = combine_single(single_partials)
    grouped_two = combine_two(two_partials)
    pivot = grouping.pivot_with_margins(grouped_two)
    top_10 = grouping.top10(grouped)
 
    missing_report = grouping.missing_value_report(missing_counts)
 
    out_dir = config["output_folder"]
    os.makedirs(out_dir, exist_ok=True)

    grouped.to_csv(os.path.join(out_dir, "grouped.csv"), index=False)
    grouped_two.to_csv(os.path.join(out_dir, "grouped_two.csv"), index=False)
    pivot.to_csv(os.path.join(out_dir, "pivot.csv"))
    top_10.to_csv(os.path.join(out_dir, "top10.csv"), index=False)
    missing_report.to_csv(os.path.join(out_dir, "missing_value_report.csv"), index=False)
 
 # Ensure output directory exists
    os.makedirs(config["output_folder"], exist_ok=True)

    # Generate bar plot (Top 10 Countries by Dutiable Value)
    plots.make_bar_plot(
        data=top_10,
        x_column=grouping.CAT_COL_1,
        y_column="sum",
        title="Top 10 Countries by Dutiable Value",
        x_label="Country of Origin (ISO3)",
        y_label="Dutiable Value (PHP)",
        output_path=os.path.join(config["output_folder"], "bar.png"),
    )

    # Prepare data & generate heatmap (excluding margins)
    heatmap_data = pivot.drop(index="Total", columns="Total", errors="ignore")
    plots.make_heatmap(
        data=heatmap_data,
        title="Dutiable Value by Country of Origin and Quarter",
        x_label="Quarter",
        y_label="Country of Origin (ISO3)",
        output_path=os.path.join(config["output_folder"], "heatmap.png"),
    )

    print("Done. Generated CSVs, bar.png, and heatmap.png in outputs/ folder.")
    print("Done. Wrote: grouped.csv, grouped_two.csv, pivot.csv, top10.csv, missing_value_report.csv")

    # 1. Initialize Audit Log
    audit = validate.AuditLog()
    audit.record(
        step="Data Loading & Aggregation",
        operation="Chunk Processing",
        rule="Read full CSV in chunks of 200,000 rows",
        rows_before=len(raw_df),
        rows_after=len(grouped)
    )
    audit.save(config["output_folder"])

    # 2. Run All Validations (Generates validation.csv)
    # Note: Pass your DataFrames and benchmark results here
    validation_passed = validate.run_all_validations(
        raw_df=raw_df,          # Adjust raw_df/selected_df based on your full pipeline
        selected_df=raw_df,
        excluded_df=pd.DataFrame(),
        grouped_df=grouped,
        pivot_df=pivot,
        loop_result=100.0,       # Replace with your actual benchmark return values
        vectorized_result=100.0,
        output_folder=config["output_folder"]
    )

    if not validation_passed:
        print("Warning: One or more validation checks failed!")

 
if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
