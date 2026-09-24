import pandas as pd
import config
import os

class Loader():
    def __init__(self, config, df):
        self.config = config
        self.df = None

    def load(self):
        path = self.config["input_path"]

        # 1. Missing file error case
        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"Input file not found: {path}. "
                "Download 2015.csv and place it in that folder (see README)."
            )

        # Read ONLY the header row (nrows=0) - fast even for a 493 MB file - so a missing column fails immediately, before the big read.
        header = pd.read_csv(path, encoding="latin-1", nrows=0)
        self._check_columns(header.columns)

        # Now read the full file, keeping only the columns we need (usecols). This saves a lot of memory versus loading every column.
        self.df = pd.read_csv(
            path,
            encoding="latin-1",
            usecols=self.config["required_columns"],
        )
        return self.df

    def describe(self):
        if self.df is None:
            raise ValueError("No data loaded. Call load() before describe().")

        summary = {
            "shape": self.df.shape,
            "dtypes": self.df.dtypes.astype(str).to_dict(),
            "missing_values": self.df.isna().sum().to_dict(),
        }

        if "tq" in self.df.columns:
            summary["tq_range"] = (self.df["tq"].min(), self.df["tq"].max())
            summary["tq_unique"] = sorted(self.df["tq"].dropna().unique().tolist())

        if "countryorigin_iso3" in self.df.columns:
            summary["n_countries"] = self.df["countryorigin_iso3"].nunique()

        if "dutiablevaluephp" in self.df.columns:
            summary["dutiablevaluephp_stats"] = (
                self.df["dutiablevaluephp"].describe().to_dict()
            )

        return summary
