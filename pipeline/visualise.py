import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

FIGURES = Path("output/figures")
COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

def savefig(name):
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / f"{name}.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path

def plot_co2_total(trend):
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (country, grp) in enumerate(trend.groupby("country")):
        ax.plot(grp["year"], grp["co2"], label=country, color=COLORS[i], linewidth=2)
    ax.set_title("Total CO₂ Emissions (Mt) – 1990–2024", fontsize=13)
    ax.set_ylabel("Million tonnes CO₂")
    ax.legend()
    ax.grid(alpha=0.3)
    return savefig("co2_total")

def plot_co2_per_capita(trend):
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (country, grp) in enumerate(trend.groupby("country")):
        ax.plot(grp["year"], grp["co2_per_capita"], label=country, color=COLORS[i], linewidth=2)
    ax.set_title("CO₂ Emissions per Capita (t) – 1990–2024", fontsize=13)
    ax.set_ylabel("Tonnes CO₂ per person")
    ax.legend()
    ax.grid(alpha=0.3)
    return savefig("co2_per_capita")

def plot_pct_change(pct, baseline_year, recent_year):
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(pct["country"], pct["co2_change_pct"],
                  color=[COLORS[i] for i in range(len(pct))])
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(f"Total CO₂ Change (%) {baseline_year}–{recent_year}", fontsize=13)
    ax.set_ylabel("% change")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    for bar, val in zip(bars, pct["co2_change_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (1 if val >= 0 else -3),
                f"{val:.1f}%", ha="center", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    return savefig("co2_pct_change")

def plot_source_breakdown(sources, recent_year):
    fig, ax = plt.subplots(figsize=(9, 5))
    width = 0.25
    x = range(len(sources))
    ax.bar([i - width for i in x], sources["coal_share"], width, label="Coal", color="#4e4e4e")
    ax.bar(list(x), sources["gas_share"], width, label="Gas", color="#f0a500")
    ax.bar([i + width for i in x], sources["oil_share"], width, label="Oil", color="#c0392b")
    ax.set_xticks(list(x))
    ax.set_xticklabels(sources["country"])
    ax.set_title(f"CO₂ Source Breakdown (%) – {recent_year}", fontsize=13)
    ax.set_ylabel("% of total CO₂")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    return savefig("co2_sources")

def run_all(results):
    by = results["baseline_year"]
    ry = results["recent_year"]
    return {
        "co2_total": plot_co2_total(results["trend"]),
        "co2_per_capita": plot_co2_per_capita(results["trend"]),
        "pct_change": plot_pct_change(results["pct_change"], by, ry),
        "sources": plot_source_breakdown(results["source_breakdown"], ry),
    }
