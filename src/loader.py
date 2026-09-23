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
