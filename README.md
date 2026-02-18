# Alberta Population & Education Spending Analysis (2012–2025)

A multi-part data science project examining Alberta's population growth and whether provincial education spending has kept pace with it. Built using open data from Statistics Canada and Alberta's published Budget Fiscal Plans.

---

## Project Structure

| Notebook | Description |
|---|---|
| [`Population Predictions Canada 2025.ipynb`](Population%20Predictions%20Canada%202025.ipynb) | Population trends analysis — growth rates, COVID impact, Alberta's share of Canada |
| [`Alberta Population Analysis and Predictions/Alberta Education Spending Comparison.ipynb`](Alberta%20Population%20Analysis%20and%20Predictions/Alberta%20Education%20Spending%20Comparison.ipynb) | Education spending across budget years (2012, 2013, 2023, 2024, 2025) — K-12 vs post-secondary |
| [`Alberta Population Analysis and Predictions/Alberta Population vs Education Spending.ipynb`](Alberta%20Population%20Analysis%20and%20Predictions/Alberta%20Population%20vs%20Education%20Spending.ipynb) | Integration analysis — did education spending grow proportionally to population? |

For full documentation including all visualizations and findings, see the [subfolder README](Alberta%20Population%20Analysis%20and%20Predictions/README.md).

---

## Data Sources

| File | Description |
|---|---|
| [`17100009.csv`](17100009.csv) | Statistics Canada, Table 17-10-0009-01 — quarterly population estimates for all provinces, 1946–present |
| [`Alberta Population Analysis and Predictions/budget_data/`](Alberta%20Population%20Analysis%20and%20Predictions/budget_data/) | Alberta Budget Fiscal Plans — expense tables (Excel) for 2023-24, 2024-25, 2025-26; PDF fiscal plans for 2012-13, 2013-14 |

---

## Key Findings

| Metric | 2012-13 / Q1 2012 | 2025-26 / Q1 2025 | Nominal Growth |
|---|---|---|---|
| Alberta Population | 3,822,425 | 4,988,181 | **+30.5%** |
| K-12 Operating Expense | $6,179M | $9,883M | **+59.9%** |
| Post-Secondary Operating Expense | $2,856M | $6,635M | **+132.3%** |
| Total Education Expense | $9,035M | $16,518M | **+82.8%** |
| Education Spending per Capita | ~$2,363 | ~$3,312 | **+40.1%** |

Education spending grew substantially faster than Alberta's population in nominal terms. Total education spending increased **82.8%** while the population grew **30.5%** — nearly 2.7× the rate of population growth. All figures are nominal (not inflation-adjusted).

---

## Tools & Libraries

- **Python 3.12**
- **pandas** — data manipulation
- **numpy** — numerical operations
- **seaborn** / **matplotlib** — visualization

---

*Population data: Statistics Canada, Table 17-10-0009-01.*
*Spending data: Alberta Budget Fiscal Plans (Government of Alberta).*
