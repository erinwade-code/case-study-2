import os
import sys
import pandas as pd

import transform

CHUNKSIZE = 200_000
REQUIRED_COLUMNS = {
    "countryorigin_iso3", "port", "tm", "dutiestaxes", "dutiablevaluephp",
}
 
 
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
 
 
