import os
import pandas as pd

def ensure_dirs(base_dir):
    artifacts = f"{base_dir}/artifacts"
    figures = f"{artifacts}/figures"
    os.makedirs(figures, exist_ok=True)
    return artifacts, figures

def load_weekly_data(path):
    df = pd.read_csv(path, parse_dates=["week"])
    df = df.sort_values("week").reset_index(drop=True)
    return df