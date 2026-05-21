# CO₂ Emissions Reporting Pipeline

A Python pipeline that ingests public environmental data, performs data quality checks, cleans and transforms the dataset, runs trend analysis across selected European countries, and produces an automated HTML report with embedded charts.

> This project demonstrates a production-style data quality and reporting workflow applied to publicly available environmental data: ingestion, QA/QC, cleaning, analysis, and automated report generation.

---

## What it does

| Step | Module | Output |
|------|--------|--------|
| Ingest | `pipeline/ingest.py` | Raw CSV downloaded from OWID |
| Clean & QA | `pipeline/clean.py` | Filtered & validated dataset, QA metrics |
| Analyse | `pipeline/analyse.py` | Trends, % changes, source breakdown, decadal averages |
| Visualise | `pipeline/visualise.py` | PNG charts in `output/figures/` |
| Report | `pipeline/report.py` | Self-contained `output/report.html` |

---

## Dataset

**CO₂ and Greenhouse Gas Emissions** – [Our World in Data](https://ourworldindata.org/co2-and-greenhouse-gas-emissions)  
Source file: [`owid-co2-data.csv`](https://github.com/owid/co2-data) (updated regularly)

Columns used: `country`, `year`, `population`, `gdp`, `co2`, `co2_per_capita`, `co2_growth_prct`, `coal_co2`, `gas_co2`, `oil_co2`, `share_global_co2`, `cumulative_co2`

---

## Countries & Period

- **Countries:** Italy, France, Germany, Spain, Netherlands  
- **Period:** 1990 – 2024  
- **Baseline for % change:** year 2000

---

## Quality checks performed

- Missing value counts for key columns (`co2`, `co2_per_capita`, `gdp`)
- Detection and removal of negative emission values
- Type coercion and invalid-value handling
- Year-range and country-scope filtering
- All QA metrics are surfaced in the final report

---

## Outputs

```
output/
├── figures/
│   ├── co2_total.png
│   ├── co2_per_capita.png
│   ├── co2_pct_change.png
│   └── co2_sources.png
├── report.html          ← self-contained, open in browser
data/processed/
└── co2_europe_clean.csv ← clean dataset ready for downstream use
```

---

## Usage

```bash
pip install -r requirements.txt

# Default run (Italy, France, Germany, Spain, Netherlands — 1990–2024)
python run.py

# Custom countries and period
python run.py --countries "Poland" "Sweden" "Austria" --year-min 2000 --year-max 2024

# Custom baseline and reference year for % change analysis
python run.py --baseline 1995 --recent 2020

# Force re-download of the raw dataset
python run.py --force-download
```

All parameters are optional and can be combined freely.

---

## Project structure

```
co2-reporting-pipeline/
├── pipeline/
│   ├── ingest.py       # download & load raw data
│   ├── clean.py        # QA checks & cleaning
│   ├── analyse.py      # metrics & trend analysis
│   ├── visualise.py    # matplotlib charts
│   └── report.py       # HTML report generation
├── run.py              # pipeline entry point
├── requirements.txt
└── README.md
```

---

## Tech stack

Python 3.10+ · pandas · matplotlib · requests

---

*Data source: Our World in Data — licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)*
