# Case Study 2

# Dataset Chosen:

## Information and Rules

### Configuration
Download the 2015.csv from https://huggingface.co/datasets/bettergovph/open-customs-data/resolve/main/yearly/csv/2015.csv?download=true, Downloaded on September 22, 2026, the file size is ~493.5 MB, so download with decent WIFI connection and storage in your unit. Place it in data/raw/ inside the project folder.

### Loader Feature
In this feature, here are the necessary data dictionaries that are important on our analysis that will be used to investigate and find summaries or description based on the 2015 Bureau of Customs open data.

| Field | Meaning | Unit | Assumptions |
|---|---|---|---|
| countryorigin_iso3 | Country the goods originated from | ISO3 country code | These goods were sourced from this country |
| tq | Year + Quarter the goods were imported | quarter code (e.g. 2015q1) | Reflects the transaction quarter, not necessarily arrival date |
| dutiablevaluephp | Customs-assessed value of the imported goods | PHP | Converted from foreign currency using the transaction's exchange rate |

## Project Structure
main.py - entry point
config.py - input path, filter values, group columns, output folder
loader.py - loads and validates the raw data
transform.py - filtering, derived columns, grouping
numpy_ops.py - NumPy comparison and plots
validate.py - validation and audit log

## Instructions:
1. Clone this repository to your computer
2. Create a virtual environment
3. Activate it
4. Install requirements
5. Download dataset file and place it in a data/ folder in the project root (it's gitignored either way)
6. Run the program

## Reminders
1. Commit regularly on your part
2. When your part is done, open a pull request so that another member can review your part before merging
