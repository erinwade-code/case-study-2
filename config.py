from pathlib import Path

# BASE_DIR = the folder that contains this config.py file.
# Anchoring paths here means the program works no matter which folder
# you run it from in the terminal.
BASE_DIR = Path(__file__).resolve().parent

# The single dictionary every other file will use.
config = {
    "input_path": str(BASE_DIR / "data" / "raw" / "2015.csv"),
    "required_columns": ["tq", "countryorigin_iso3", "dutiablevaluephp"],
    "filter_values": {},      # e.g. {"tq": ["2015q1", "2015q2"]} - agree format with transform.py owner
    "grouping_columns": [],   # e.g. ["countryorigin_iso3"]
    "output_folder": str(BASE_DIR / "outputs"),
}
