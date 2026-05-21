import base64
from pathlib import Path
from datetime import date

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CO₂ Emissions Report – Europe</title>
<style>
  body {{ font-family: 'Segoe UI', sans-serif; max-width: 960px; margin: 40px auto; color: #222; }}
  h1 {{ color: #1a5276; border-bottom: 2px solid #1a5276; padding-bottom: 8px; }}
  h2 {{ color: #1a5276; margin-top: 40px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
  th {{ background: #1a5276; color: white; padding: 8px 12px; text-align: left; }}
  td {{ padding: 7px 12px; border-bottom: 1px solid #ddd; }}
  tr:nth-child(even) {{ background: #f4f6f9; }}
  img {{ width: 100%; border: 1px solid #ddd; border-radius: 4px; margin: 12px 0; }}
  .qa-box {{ background: #f0f4f8; border-left: 4px solid #1a5276; padding: 12px 16px; margin: 16px 0; }}
  .qa-box p {{ margin: 4px 0; }}
  footer {{ margin-top: 60px; font-size: 0.85em; color: #888; border-top: 1px solid #ddd; padding-top: 12px; }}
</style>
</head>
<body>
<h1>CO₂ Emissions Reporting Pipeline – Europe</h1>
<p>Generated: {date} &nbsp;|&nbsp; Source: <a href="https://ourworldindata.org/co2-and-greenhouse-gas-emissions">Our World in Data</a></p>
<p>Countries: {countries} &nbsp;|&nbsp; Period: {year_min}–{year_max}</p>

<h2>1. Data Quality Summary</h2>
<div class="qa-box">
  <p><strong>Rows after filter:</strong> {qa_rows}</p>
  <p><strong>Missing co2 values:</strong> {qa_missing_co2}</p>
  <p><strong>Missing co2_per_capita:</strong> {qa_missing_pc}</p>
  <p><strong>Missing gdp values:</strong> {qa_missing_gdp}</p>
  <p><strong>Negative co2 values (removed):</strong> {qa_negative}</p>
</div>

<h2>2. Total CO₂ Emissions (1990–2024)</h2>
<img src="{img_total}" alt="Total CO2">

<h2>3. CO₂ Emissions per Capita (1990–2024)</h2>
<img src="{img_pc}" alt="CO2 per capita">

<h2>4. Total Emissions Change – 2000 to 2023</h2>
<img src="{img_pct}" alt="Percent change">
{table_pct}

<h2>5. CO₂ Source Breakdown (2023)</h2>
<img src="{img_src}" alt="Source breakdown">
{table_src}

<h2>6. Decadal Average Emissions (Mt CO₂)</h2>
{table_dec}

<footer>Data pipeline built with Python · pandas · matplotlib · Source: OWID</footer>
</body>
</html>"""

def img_to_b64(path):
    data = Path(path).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode()

def df_to_html(df):
    return df.to_html(index=False, border=0, classes="", float_format=lambda x: f"{x:.2f}")

def generate(qa, results, figure_paths, countries, year_min, year_max):
    by = results["baseline_year"]
    ry = results["recent_year"]
    pct = results["pct_change"].copy()
    pct.columns = ["Country", "CO₂ Change (%)", "CO₂/capita Change (%)"]
    src = results["source_breakdown"][["country","co2","co2_per_capita","coal_share","gas_share","oil_share"]].copy()
    src.columns = ["Country","CO₂ (Mt)","CO₂/capita (t)","Coal (%)","Gas (%)","Oil (%)"]
    dec = results["decadal_avg"].pivot(index="decade", columns="country", values="co2").reset_index()
    dec.rename(columns={"decade": "Decade"}, inplace=True)
    html = TEMPLATE.format(
        date=date.today().strftime("%d %B %Y"),
        countries=", ".join(countries),
        year_min=year_min, year_max=year_max,
        qa_rows=qa["total_rows"],
        qa_missing_co2=qa["missing_co2"],
        qa_missing_pc=qa["missing_co2_per_capita"],
        qa_missing_gdp=qa["missing_gdp"],
        qa_negative=qa["negative_co2"],
        img_total=img_to_b64(figure_paths["co2_total"]),
        img_pc=img_to_b64(figure_paths["co2_per_capita"]),
        img_pct=img_to_b64(figure_paths["pct_change"]),
        img_src=img_to_b64(figure_paths["sources"]),
        table_pct=df_to_html(pct),
        table_src=df_to_html(src),
        table_dec=df_to_html(dec),
    )
    out = Path("output/report.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out
