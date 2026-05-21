import pandas as pd

def co2_trend(df):
    return df.groupby(["country", "year"])[["co2", "co2_per_capita"]].sum().reset_index()

def pct_change(df, baseline_year, recent_year):
    base = df[df["year"] == baseline_year][["country", "co2", "co2_per_capita"]].set_index("country")
    recent = df[df["year"] == recent_year][["country", "co2", "co2_per_capita"]].set_index("country")
    delta = ((recent - base) / base * 100).round(2)
    delta.columns = ["co2_change_pct", "co2_per_capita_change_pct"]
    return delta.reset_index()

def source_breakdown(df, recent_year):
    latest = df[df["year"] == recent_year].copy()
    latest["coal_share"] = (latest["coal_co2"] / latest["co2"] * 100).round(2)
    latest["gas_share"] = (latest["gas_co2"] / latest["co2"] * 100).round(2)
    latest["oil_share"] = (latest["oil_co2"] / latest["co2"] * 100).round(2)
    return latest[["country", "co2", "co2_per_capita", "coal_share", "gas_share", "oil_share"]]

def decadal_avg(df):
    df = df.copy()
    df["decade"] = (df["year"] // 10) * 10
    return df.groupby(["country", "decade"])["co2"].mean().round(2).reset_index()

def run_all(df, baseline_year, recent_year):
    return {
        "trend": co2_trend(df),
        "pct_change": pct_change(df, baseline_year, recent_year),
        "source_breakdown": source_breakdown(df, recent_year),
        "decadal_avg": decadal_avg(df),
        "baseline_year": baseline_year,
        "recent_year": recent_year,
    }
