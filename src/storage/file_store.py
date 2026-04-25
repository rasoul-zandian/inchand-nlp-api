import json
from pathlib import Path

STORE_PATH = Path("data/processed/summary_store.json")


def ensure_store_file():
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not STORE_PATH.exists():
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)


def load_store():
    ensure_store_file()

    with open(STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_store(data: dict):
    ensure_store_file()

    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_summary_record(product_id: str):
    store = load_store()
    return store.get(str(product_id))


def save_summary_record(product_id: str, summary_data: dict):
    store = load_store()
    store[str(product_id)] = summary_data
    save_store(store)