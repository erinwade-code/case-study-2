# Case Study 2

# Dataset Chosen: 2015.csv

## Information and Rules
1. feature/data-loader:Implemented chunked CSV ingestion in `src/loader.py` to handle large datasets efficiently without overflowing memory.
2. feature/data-transformation: Created filtering rules and derived calculated metrics inside `src/transform.py` to clean and standardize raw records.
3. feature/grouping-aggregations: Built grouping methods in `src/grouping.py` for single/double-variable aggregations, pivot table generation, and missing value reporting.
4. feature/numpy-benchmarking: Developed vectorized and loop-based performance comparisons in `src/numpy_ops.py` using fixed random seeds.
5. feature/data-validation: Implemented automated audit trail logging (`AuditLog`) and structural integrity checks in `src/validate.py`.
6. feature/numpy_ops: Designed automated charting utilities in `src/plots.py` to render and export heatmap and bar chart visualizations.

### Configuration
Download the 2015.csv from https://huggingface.co/datasets/bettergovph/open-customs-data/resolve/main/yearly/csv/2015.csv?download=true, Downloaded on September 22, 2026, the file size is ~493.5 MB, so download with decent WIFI connection and storage in your unit. Place it in data/raw/ inside the project folder.

### Loading the dataset
In this feature, here are the necessary data dictionaries that are important on our analysis that will be used to investigate and find summaries or description based on the 2015 Bureau of Customs open data.

| Field | Meaning | Unit | Assumptions |
|---|---|---|---|
| countryorigin_iso3 | Country the goods originated from | ISO3 country code | These goods were sourced from this country |
| tq | Year + Quarter the goods were imported | quarter code (e.g. 2015q1) | Reflects the transaction quarter, not necessarily arrival date |
| dutiablevaluephp | Customs-assessed value of the imported goods | PHP | Converted from foreign currency using the transaction's exchange rate |

## Project Structure
1. main.py - entry point
2. config.py - input path, filter values, group columns, output folder
3. loader.py - loads and validates the raw data
4. transform.py - filtering, derived columns, grouping
5. numpy_ops.py - NumPy comparison and plots
6. validate.py - validation and audit log

## Instructions:
1. Clone this repository to your computer
2. Create a virtual environment
3. Activate it
4. Install requirements using pip
5. Download dataset file and place it in a data/ folder in the project root (it's gitignored either way)
6. Run the program by typing "python main.py"



