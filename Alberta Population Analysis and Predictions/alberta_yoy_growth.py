"""
alberta_yoy_growth.py
---------------------
Builds a year-over-year (YoY) population growth dataframe for Alberta
using Q1 (January) snapshots from Statistics Canada Table 17-10-0009-01.

Output columns:
    Year                – Calendar year (2012–2025)
    Population          – Alberta population as of Q1 (January)
    YoY_Change          – Absolute population change vs. prior year
    YoY_Growth_Pct      – Percentage population change vs. prior year
    Cumulative_Growth   – Cumulative absolute growth since 2012
    Cumulative_Growth_Pct – Cumulative percentage growth since 2012
    Canada_Population   – Canada-wide population as of Q1
    AB_Share_Pct        – Alberta's share of Canada's total population (%)

Data source: Statistics Canada, Table 17-10-0009-01
"""

import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration – resolve paths relative to this script's directory
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / "17100009.csv"
START_YEAR = 2012
END_YEAR = 2025
OUTPUT_CSV = SCRIPT_DIR / "alberta_yoy_growth.csv"


def load_raw_data(path: str) -> pd.DataFrame:
    """Load the raw Statistics Canada CSV and parse the date column."""
    df = pd.read_csv(path)
    df["REF_DATE"] = pd.to_datetime(df["REF_DATE"], format="%Y-%m")
    df["VALUE"] = pd.to_numeric(df["VALUE"], errors="coerce")
    return df


def filter_q1_data(df: pd.DataFrame, geo: str, start: int, end: int) -> pd.DataFrame:
    """
    Filter for Q1 (January) rows of a specific geography,
    within the given year range (inclusive).
    """
    mask = (
        (df["GEO"] == geo)
        & (df["REF_DATE"].dt.month == 1)
        & (df["REF_DATE"].dt.year >= start)
        & (df["REF_DATE"].dt.year <= end)
    )
    return df.loc[mask].copy()


def build_yoy_dataframe(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Construct the year-over-year growth dataframe for Alberta,
    enriched with Canada-level context.

    Strategy:
        1. Pull Q1-only rows for Alberta and Canada independently.
        2. Merge on year so each row has both populations side-by-side.
        3. Derive all growth and share columns from that merged set.
    """
    # --- Alberta Q1 data ---
    ab = filter_q1_data(raw, "Alberta", START_YEAR, END_YEAR)
    ab["Year"] = ab["REF_DATE"].dt.year
    ab = ab[["Year", "VALUE"]].rename(columns={"VALUE": "Population"})
    ab = ab.sort_values("Year").reset_index(drop=True)

    # --- Canada Q1 data (for national share calculation) ---
    ca = filter_q1_data(raw, "Canada", START_YEAR, END_YEAR)
    ca["Year"] = ca["REF_DATE"].dt.year
    ca = ca[["Year", "VALUE"]].rename(columns={"VALUE": "Canada_Population"})
    ca = ca.sort_values("Year").reset_index(drop=True)

    # --- Merge Alberta + Canada on Year ---
    yoy = pd.merge(ab, ca, on="Year", how="left")

    # --- Year-over-year metrics ---
    yoy["YoY_Change"] = yoy["Population"].diff()
    yoy["YoY_Growth_Pct"] = yoy["Population"].pct_change() * 100

    # --- Cumulative growth relative to the first year (2012) ---
    base_pop = yoy["Population"].iloc[0]
    yoy["Cumulative_Growth"] = yoy["Population"] - base_pop
    yoy["Cumulative_Growth_Pct"] = ((yoy["Population"] - base_pop) / base_pop) * 100

    # --- Alberta's share of Canada's population ---
    yoy["AB_Share_Pct"] = (yoy["Population"] / yoy["Canada_Population"]) * 100

    # --- Round percentages for readability ---
    pct_cols = ["YoY_Growth_Pct", "Cumulative_Growth_Pct", "AB_Share_Pct"]
    yoy[pct_cols] = yoy[pct_cols].round(2)

    return yoy


def main():
    """Entry point: load, transform, display, and export."""
    raw = load_raw_data(DATA_PATH)
    yoy = build_yoy_dataframe(raw)

    # Pretty-print to console (with comma-formatted numbers)
    print("\n=== Alberta Year-over-Year Population Growth (2012–2025) ===\n")
    print(yoy.to_string(index=False))

    # Export to CSV alongside the source data
    yoy.to_csv(OUTPUT_CSV, index=False)
    print(f"\n✅ Exported to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
