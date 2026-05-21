import requests
import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/owid-co2-data.csv")
SOURCE_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

COLUMNS = [
    "country", "iso_code", "year", "population", "gdp",
    "co2", "co2_per_capita", "co2_growth_prct",
    "coal_co2", "gas_co2", "oil_co2",
    "share_global_co2", "cumulative_co2",
]

def download_raw(force=False):
    if RAW_PATH.exists() and not force:
        return
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(SOURCE_URL, timeout=60)
    r.raise_for_status()
    RAW_PATH.write_bytes(r.content)

def load_raw(force=False):
    download_raw(force)
    return pd.read_csv(RAW_PATH, usecols=COLUMNS)
