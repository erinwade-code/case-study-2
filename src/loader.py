import os
from typing import Any

import pandas as pd


class Loader:
    """Loads the 2015 customs CSV, validates required columns, and summarises it."""

    def __init__(self, config: dict[str, Any]) -> None:
        # config is the dictionary from config.py, passed in by main.py:
        #     Loader(config)
        self.config: dict[str, Any] = config
        self.df: pd.DataFrame | None = None  # filled in by load()

    def _check_columns(self, available: pd.Index | list[str]) -> None:
        """Raise a clear error if any required column is missing."""
        required: list[str] = self.config["required_columns"]
        missing: list[str] = [col for col in required if col not in available]
        if missing:
            raise ValueError(
                f"Missing required column(s): {missing}. "
                f"Columns available: {list(available)}"
            )

    def load(self) -> pd.DataFrame:
        path: str = self.config["input_path"]

        # 1. Missing file error case (look-before-you-leap, no try/except).
        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"Input file not found: {path}. "
                "Download 2015.csv and place it in that folder (see README)."
            )

        # 2. Read ONLY the header row so a missing column fails before the big read.
        header: pd.DataFrame = pd.read_csv(path, encoding="latin-1", nrows=0)
        self._check_columns(header.columns)

        # 3. Read the full file, keeping only the columns we need.
        self.df = pd.read_csv(
            path,
            encoding="latin-1",
            usecols=self.config["required_columns"],
        )
        return self.df

    def validate_columns(self) -> pd.DataFrame:
        """Check the loaded DataFrame has every required column and keep only those."""
        if self.df is None:
            raise ValueError("No data loaded. Call load() before validate_columns().")

        self._check_columns(self.df.columns)
        self.df = self.df[self.config["required_columns"]]
        return self.df

    def describe(self) -> dict[str, Any]:
        """Return a summary dictionary (main.py decides whether to print or save it)."""
        if self.df is None:
            raise ValueError("No data loaded. Call load() before describe().")

        summary: dict[str, Any] = {
            "shape": self.df.shape,
            "dtypes": self.df.dtypes.astype(str).to_dict(),
            "missing_values": self.df.isna().sum().to_dict(),
        }

        if "tq" in self.df.columns:
            summary["tq_unique"] = sorted(self.df["tq"].dropna().unique().tolist())

        if "countryorigin_iso3" in self.df.columns:
            summary["n_countries"] = self.df["countryorigin_iso3"].nunique()

        if "dutiablevaluephp" in self.df.columns:
            summary["dutiablevaluephp_stats"] = (
                self.df["dutiablevaluephp"].describe().to_dict()
            )

        return summary
