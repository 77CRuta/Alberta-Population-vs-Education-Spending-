# Alberta Population Analysis (2012–2025)

An analysis of Alberta's population trends using quarterly data from **Statistics Canada (Table 17-10-0009-01)**. This project examines population growth, quarterly growth rates, Alberta's share of Canada's total population, and year-over-year comparisons.

## Data

- **Source**: [Statistics Canada — Table 17-10-0009-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)
- **File**: [`17100009.csv`](17100009.csv) — Quarterly population estimates for Canada and all provinces/territories, dating back to 1946.
- **Analysis Notebook**: [`Population Predictions Canada 2025.ipynb`](Population%20Predictions%20Canada%202025.ipynb)

## Key Findings

| Metric | Value |
|---|---|
| Alberta Population (Q1 2012) | **3,822,425** |
| Alberta Population (Q1 2025) | **4,988,181** |
| Total Growth (2012–2025) | **+1,165,756 (~30.5%)** |
| Avg. Quarterly Growth Rate | **0.514%** |
| Peak Quarterly Growth Rate | **1.356%** *(Q4 2023)* |
| Lowest Quarterly Growth Rate | **0.046%** *(Q3 2020 — COVID-19 impact)* |
| Alberta's National Share (1951) | **6.7%** |
| Alberta's National Share (2025) | **12.1%** |
| National Share Change | **+5.4 percentage points** |

### Summary

Alberta's population has grown steadily over the past 13 years, accelerating sharply after 2020. The province added over **1.1 million people** between 2012 and 2025 — a roughly **30% increase**. The most dramatic growth occurred in 2023, when quarterly growth rates exceeded **1%** — more than double the long-term average. Meanwhile, the COVID-19 pandemic in 2020 nearly halted population growth entirely, with Q3 2020 recording the lowest quarterly growth rate of just **0.046%**.

Alberta's weight within Canada has grown substantially. In 1951, the province represented just **6.7%** of Canada's total population. By 2025, that figure had nearly doubled to **12.1%**, reflecting the province's consistent draw of interprovincial and international migration.

---

## Visualizations

### 1. Alberta Population Growth (2012–2025)

A line chart showing Alberta's total population over time. The trend reveals consistent upward growth with a visible acceleration in the 2022–2025 period.

![Alberta Population Growth](plots/alberta_population_growth.png)

---

### 2. Quarterly Population Growth Rate

A bar chart illustrating the quarter-over-quarter percentage change in Alberta's population.

- 🟢 **Green bars** = high growth (≥ 1.0%)
- 🔵 **Blue bars** = moderate growth
- 🔴 **Red bars** = negative or near-zero growth
- 🟠 **Orange dashed line** = average quarterly growth rate (~0.51%)

The chart clearly shows the COVID-19 dip in 2020 and the post-pandemic surge in 2022–2024.

![Quarterly Growth Rate](plots/quarterly_growth_rate.png)

---

### 3. Alberta's Share of Canada's Total Population

A line chart tracking the percentage of Canada's population living in Alberta, from 1951 to the present. Alberta's share has risen from **6.7%** to **12.1%**, highlighting the province's growing demographic significance.

![Alberta Population Share](plots/alberta_population_share.png)

---

### 4. Year-over-Year Growth Analysis

Two-panel bar charts using Q1 (January) data for clean annual comparisons:

- **Top panel**: Absolute year-over-year population change
- **Bottom panel**: Year-over-year percentage growth rate

This perspective smooths out quarterly fluctuations and reveals long-term trends. The 2023 and 2024 bars show population gains of historic magnitude.

![YoY Growth Analysis](plots/yoy_growth_analysis.png)

---

## Methodology

1. **Data Loading**: The raw CSV from Statistics Canada is loaded into a pandas DataFrame.
2. **Filtering**: Data is filtered for `GEO == 'Alberta'` and the relevant date ranges.
3. **Derived Metrics**:
   - `Population_Change` = quarter-over-quarter absolute change (`.diff()`)
   - `Growth_Rate_Pct` = quarter-over-quarter percentage change (`.pct_change() * 100`)
   - `AB_Share_Pct` = `(Alberta population / Canada population) * 100`
   - `YoY_Change` and `YoY_Growth_Pct` = annual comparisons using Q1 data only
4. **Visualization**: Charts are generated using `matplotlib` and `seaborn`.

## Tools & Libraries

- **Python 3.12**
- **pandas** — data manipulation
- **numpy** — numerical operations
- **seaborn** / **matplotlib** — visualization

---

*Data Source: Statistics Canada, Table 17-10-0009-01.*
