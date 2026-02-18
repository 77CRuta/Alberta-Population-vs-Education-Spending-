"""
Generates the 3 integration charts for Alberta Population vs Education Spending.
Run from within the 'Alberta Population Analysis and Predictions' directory.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Dark infographic theme ───────────────────────────────────────────────────
sns.set_theme(style='darkgrid', context='notebook', font_scale=1.15)
plt.rcParams.update({
    'figure.facecolor': '#0D1117',
    'axes.facecolor':   '#161B22',
    'axes.edgecolor':   '#30363D',
    'axes.labelcolor':  '#E6EDF3',
    'text.color':       '#E6EDF3',
    'xtick.color':      '#8B949E',
    'ytick.color':      '#8B949E',
    'grid.color':       '#21262D',
    'grid.alpha':       0.6,
    'font.family':      'sans-serif',
    'savefig.facecolor':'#0D1117',
})

POP_COLOR  = '#F778BA'
K12_COLOR  = '#58A6FF'
PS_COLOR   = '#56D364'
TOT_COLOR  = '#FFB703'

# ── Population data ──────────────────────────────────────────────────────────
pop_raw = pd.read_csv('17100009.csv')
pop_raw['REF_DATE'] = pd.to_datetime(pop_raw['REF_DATE'])

ab_pop = pop_raw[
    (pop_raw['GEO'] == 'Alberta') &
    (pop_raw['REF_DATE'].dt.month == 1) &
    (pop_raw['REF_DATE'].dt.year.between(2012, 2025))
][['REF_DATE', 'VALUE']].copy()
ab_pop.columns = ['Date', 'Population']
ab_pop['Year'] = ab_pop['Date'].dt.year
ab_pop = ab_pop[['Year', 'Population']].reset_index(drop=True)

# ── Spending data + merge ────────────────────────────────────────────────────
spending = pd.DataFrame([
    {'Fiscal_Year': '2012-13', 'Year': 2012, 'K12_M': 6179,  'PostSec_M': 2856},
    {'Fiscal_Year': '2013-14', 'Year': 2013, 'K12_M': 6210,  'PostSec_M': 2682},
    {'Fiscal_Year': '2023-24', 'Year': 2023, 'K12_M': 8836,  'PostSec_M': 5604},
    {'Fiscal_Year': '2024-25', 'Year': 2024, 'K12_M': 9252,  'PostSec_M': 6305},
    {'Fiscal_Year': '2025-26', 'Year': 2025, 'K12_M': 9883,  'PostSec_M': 6635},
])
spending['Total_M'] = spending['K12_M'] + spending['PostSec_M']

df = spending.merge(ab_pop, on='Year', how='left')
df['K12_PerCapita']     = (df['K12_M']     * 1_000_000) / df['Population']
df['PostSec_PerCapita'] = (df['PostSec_M'] * 1_000_000) / df['Population']
df['Total_PerCapita']   = (df['Total_M']   * 1_000_000) / df['Population']

base = df.iloc[0]
df['Pop_Index']     = (df['Population']  / base['Population'])  * 100
df['K12_Index']     = (df['K12_M']       / base['K12_M'])       * 100
df['PostSec_Index'] = (df['PostSec_M']   / base['PostSec_M'])   * 100
df['Total_Index']   = (df['Total_M']     / base['Total_M'])     * 100

# ── CHART 1: Indexed Growth ──────────────────────────────────────────────────
era1 = df[df['Year'].isin([2012, 2013])]
era2 = df[df['Year'].isin([2023, 2024, 2025])]

series = [
    ('Pop_Index',     POP_COLOR, 'o', 'Population'),
    ('K12_Index',     K12_COLOR, 's', 'K-12 Spending'),
    ('PostSec_Index', PS_COLOR,  '^', 'Post-Secondary Spending'),
    ('Total_Index',   TOT_COLOR, 'D', 'Total Education Spending'),
]

fig, ax = plt.subplots(figsize=(14, 7))

for col, color, marker, label in series:
    ax.plot(era1['Year'], era1[col], color=color, linewidth=3,
            marker=marker, markersize=11, zorder=5, label=label)
    ax.plot(era2['Year'], era2[col], color=color, linewidth=3,
            marker=marker, markersize=11, zorder=5)

ax.axhline(100, color='#8B949E', linewidth=1.2, linestyle='--',
           alpha=0.55, label='2012-13 Baseline (= 100)')
ax.axvspan(2013.4, 2022.6, alpha=0.07, color='#8B949E', zorder=1)
ax.text(2018, 109, 'Data gap\n2014 - 2022', ha='center', fontsize=11,
        color='#8B949E', style='italic')

for col, color, _, _ in series:
    val = df.iloc[-1][col]
    ax.text(2025.25, val, f'{val:.0f}', color=color,
            fontsize=10, fontweight='bold', va='center')

ax.set_xlim(2011, 2027)
ax.set_xticks(df['Year'].tolist())
ax.set_xlabel('Calendar Year (Q1 population snapshot)', fontsize=13, labelpad=10)
ax.set_ylabel('Index  (2012-13 = 100)', fontsize=13, labelpad=10)
ax.set_title(
    'Alberta: Population Growth vs. Education Spending\n'
    'Indexed to 2012-13 = 100  |  Nominal figures',
    fontsize=18, fontweight='bold', pad=20, color='white'
)

leg = ax.legend(fontsize=12, loc='upper left', framealpha=0.7, edgecolor='#30363D')
leg.get_frame().set_facecolor('#161B22')
for t in leg.get_texts():
    t.set_color('#E6EDF3')

sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig('budget_data/integration_indexed_growth.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved -> budget_data/integration_indexed_growth.png')

# ── CHART 2: Per-Capita Spending ─────────────────────────────────────────────
labels = df['Fiscal_Year'].values
x = np.arange(len(labels))
w = 0.38

fig, ax = plt.subplots(figsize=(14, 7))

bars1 = ax.bar(x - w / 2, df['K12_PerCapita'],    w, label='K-12',
               color=K12_COLOR, edgecolor='#0D1117', linewidth=1.5)
bars2 = ax.bar(x + w / 2, df['PostSec_PerCapita'], w, label='Post-Secondary',
               color=PS_COLOR,  edgecolor='#0D1117', linewidth=1.5)

for bars, color in [(bars1, K12_COLOR), (bars2, PS_COLOR)]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 18,
                f'${h:,.0f}', ha='center', va='bottom',
                fontsize=9, fontweight='bold', color=color)

gap_y = df['K12_PerCapita'].max() * 0.62
ax.axvline(1.5, color='#8B949E', linewidth=1.2, linestyle=':', alpha=0.55)
ax.text(1.5, gap_y, '9-year\ndata gap', ha='center', va='center',
        fontsize=10, color='#8B949E', style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#161B22',
                  edgecolor='#30363D', alpha=0.85))

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
ax.set_ylabel('Spending per Capita ($)', fontsize=13, labelpad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
ax.set_title(
    'Alberta: Education Spending per Capita\n'
    'K-12 vs Post-Secondary  |  Nominal figures',
    fontsize=18, fontweight='bold', pad=20, color='white'
)

leg = ax.legend(fontsize=13, loc='upper left', framealpha=0.7, edgecolor='#30363D')
leg.get_frame().set_facecolor('#161B22')
for t in leg.get_texts():
    t.set_color('#E6EDF3')

sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig('budget_data/integration_per_capita.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved -> budget_data/integration_per_capita.png')

# ── CHART 3: Growth Rates Lollipop ───────────────────────────────────────────
first, last = df.iloc[0], df.iloc[-1]

metrics = [
    'Population',
    'K-12 Spending',
    'Post-Secondary\nSpending',
    'Total Education\nSpending',
]
pcts = [
    (last['Population']  / first['Population']  - 1) * 100,
    (last['K12_M']       / first['K12_M']        - 1) * 100,
    (last['PostSec_M']   / first['PostSec_M']    - 1) * 100,
    (last['Total_M']     / first['Total_M']      - 1) * 100,
]
colors = [POP_COLOR, K12_COLOR, PS_COLOR, TOT_COLOR]

fig, ax = plt.subplots(figsize=(12, 6))
y = np.arange(len(metrics))

for i in range(len(metrics)):
    ax.hlines(y[i], 0, pcts[i], color=colors[i], linewidth=4, alpha=0.85)
    ax.scatter(pcts[i], y[i], color=colors[i], s=280, zorder=5,
               edgecolor='#0D1117', linewidth=2)
    ax.text(pcts[i] + 3, y[i], f'+{pcts[i]:.1f}%',
            va='center', fontsize=14, fontweight='bold', color=colors[i])

pop_pct = pcts[0]
ax.axvline(pop_pct, color=POP_COLOR, linewidth=1.5, linestyle='--', alpha=0.45)
ax.text(pop_pct + 1, len(metrics) - 0.55,
        f'Population\ngrowth ({pop_pct:.1f}%)',
        color=POP_COLOR, fontsize=9, alpha=0.85)

ax.set_yticks(y)
ax.set_yticklabels(metrics, fontsize=13, fontweight='bold')
ax.set_xlabel('Growth from 2012-13 Baseline (%)', fontsize=13, labelpad=10)
ax.set_xlim(-5, max(pcts) * 1.3)
ax.set_title(
    'Education Spending vs. Population Growth\n'
    '2012-13 to 2025-26  |  Nominal figures',
    fontsize=18, fontweight='bold', pad=20, color='white'
)
ax.axvline(0, color='#30363D', linewidth=1)

sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.savefig('budget_data/integration_growth_rates.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved -> budget_data/integration_growth_rates.png')

# ── Export CSV ───────────────────────────────────────────────────────────────
export_cols = [
    'Fiscal_Year', 'Year', 'Population',
    'K12_M', 'PostSec_M', 'Total_M',
    'K12_PerCapita', 'PostSec_PerCapita', 'Total_PerCapita',
    'Pop_Index', 'K12_Index', 'PostSec_Index', 'Total_Index',
]
df[export_cols].to_csv('budget_data/population_vs_spending.csv', index=False)
print('Saved -> budget_data/population_vs_spending.csv')
print('Done.')
