import pandas as pd
from pathlib import Path

NUMERIC_COLS = ["co2", "co2_per_capita", "co2_growth_prct",
                "coal_co2", "gas_co2", "oil_co2",
                "share_global_co2", "cumulative_co2"]
PROCESSED_PATH = Path("data/processed/co2_europe_clean.csv")

def run_qa(df):
    return {
        "total_rows": len(df),
        "missing_co2": int(df["co2"].isna().sum()),
        "missing_co2_per_capita": int(df["co2_per_capita"].isna().sum()),
        "missing_gdp": int(df["gdp"].isna().sum()),
        "negative_co2": int((df["co2"] < 0).sum()),
        "year_range": (int(df["year"].min()), int(df["year"].max())),
    }

def clean(df, countries, year_min, year_max):
    df = df[df["country"].isin(countries)].copy()
    df = df[(df["year"] >= year_min) & (df["year"] <= year_max)]
    df[NUMERIC_COLS] = df[NUMERIC_COLS].apply(pd.to_numeric, errors="coerce")
    df = df.dropna(subset=["co2", "co2_per_capita"])
    df = df[df["co2"] >= 0]
    df = df.sort_values(["country", "year"]).reset_index(drop=True)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    return df

def load_clean(df_raw, countries, year_min, year_max):
    qa = run_qa(df_raw[df_raw["country"].isin(countries)])
    df = clean(df_raw, countries, year_min, year_max)
    return df, qa
