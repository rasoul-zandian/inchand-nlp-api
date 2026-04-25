import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/sample/sample_comments.csv")


def load_comments():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Comments file not found at: {DATA_PATH}")
    return pd.read_csv(DATA_PATH)


def get_comments_by_product_id(product_id: str):
    df = load_comments()

    df["product_id"] = df["product_id"].astype(str)

    product_comments = df[df["product_id"] == str(product_id)].copy()

    return product_comments
