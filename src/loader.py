import pandas as pd
import config
import os

class Loader():
    def __init__(self, config, df):
        self.config = config
        self.df = None

    def load(self):
        path = self.config["input_path"]
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        self.df = pd.read_csv(path, encoding="latin-1")
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
