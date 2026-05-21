import argparse
from pipeline.ingest import load_raw
from pipeline.clean import load_clean
from pipeline.analyse import run_all as analyse
from pipeline.visualise import run_all as visualise
from pipeline.report import generate

DEFAULT_COUNTRIES = ["Italy", "France", "Germany", "Spain", "Netherlands"]

parser = argparse.ArgumentParser(description="CO2 Reporting Pipeline")
parser.add_argument("--countries", nargs="+", default=DEFAULT_COUNTRIES)
parser.add_argument("--year-min", type=int, default=1990)
parser.add_argument("--year-max", type=int, default=2024)
parser.add_argument("--baseline", type=int, default=2000)
parser.add_argument("--recent", type=int, default=2023)
parser.add_argument("--force-download", action="store_true")
args = parser.parse_args()

df_raw = load_raw(force=args.force_download)
df, qa = load_clean(df_raw, args.countries, args.year_min, args.year_max)
results = analyse(df, args.baseline, args.recent)
figures = visualise(results)
report_path = generate(qa, results, figures, args.countries, args.year_min, args.year_max)
print(f"Pipeline complete → {report_path}")
