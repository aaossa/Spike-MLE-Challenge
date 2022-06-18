from pathlib import Path

import joblib
import pandas as pd


def save_dataframe(*dfs, dst=None):
    if dst is None:
        dst = "/tmp/airflow/data"
    dst = Path(dst)
    for df in dfs:
        df.to_csv(dst / f"{df.name}.csv", sep=",", index=False)


def save_model(name, model, dst=None):
    if dst is None:
        dst = "/tmp/airflow/models"
    joblib.dump(model, Path(dst) / f"{name}.joblib")


def load_dataframe(*names, src=None):
    if src is None:
        src = "/tmp/airflow/data"
    src = Path(src)
    return [
        pd.read_csv(src / f"{name}.csv")
        for name in names
    ]
