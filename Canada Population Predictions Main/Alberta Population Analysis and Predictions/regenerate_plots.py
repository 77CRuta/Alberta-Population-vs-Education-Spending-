"""
regenerate_plots.py
───────────────────
Regenerates all 13 charts in plots/ using a unified
Dark Grey + Gold color scheme.

Usage:
    python regenerate_plots.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors
import seaborn as sns
from pathlib import Path

# ═══ UNIFIED DARK GREY + GOLD THEME ════════════════════════════════════════
BG_FIG   = '#1A1A1A'   # figure outer background
BG_AX    = '#242424'   # axes / plot area
C_EDGE   = '#3A3A3A'   # axes border
C_GRID   = '#2E2E2E'   # gridlines
C_TEXT   = '#E8DFC8'   # main text (warm cream)
C_TICK   = '#8A8070'   # tick labels (muted warm grey)

# Gold spectrum — data series
GOLD_1   = '#F5C518'   # bright gold  — primary / highlight
GOLD_2   = '#D4A017'   # rich gold
GOLD_3   = '#C9984A'   # warm amber
GOLD_4   = '#A07820'   # dark gold / bronze
GOLD_DIM = '#6B5B35'   # dim bronze  — secondary / background data
C_NEG    = '#4A3B28'   # very dark bronze — negative values

# Per-budget-year shading for donut titles (older = darker, newer = brighter)
BUDGET_YEAR_PALETTE = {
    'Budget 2012': GOLD_DIM,
    'Budget 2013': '#8B7040',
    'Budget 2023': GOLD_3,
    'Budget 2024': GOLD_2,
    'Budget 2025': GOLD_1,
}

THEME_RC = {
    'figure.facecolor':  BG_FIG,
    'axes.facecolor':    BG_AX,
    'axes.edgecolor':    C_EDGE,
    'axes.labelcolor':   C_TEXT,
    'text.color':        C_TEXT,
    'xtick.color':       C_TICK,
    'ytick.color':       C_TICK,
    'grid.color':        C_GRID,
    'grid.alpha':        0.8,
    'font.family':       'sans-serif',
    'savefig.facecolor': BG_FIG,
    'legend.facecolor':  BG_AX,
    'legend.edgecolor':  C_EDGE,
}

SCRIPT_DIR = Path(__file__).resolve().parent
PLOTS_DIR  = SCRIPT_DIR / 'plots'
DATA_CSV   = SCRIPT_DIR / '17100009.csv'


# ── Helpers ─────────────────────────────────────────────────────────────────

def apply_theme():
    sns.set_theme(style='darkgrid', context='notebook', font_scale=1.15)
    plt.rcParams.update(THEME_RC)


def style_legend(leg):
    leg.get_frame().set_facecolor(BG_AX)
    leg.get_frame().set_edgecolor(C_EDGE)
    for t in leg.get_texts():
        t.set_color(C_TEXT)


# ── Data loading ─────────────────────────────────────────────────────────────

def load_population():
    df = pd.read_csv(DATA_CSV)
    df['REF_DATE'] = pd.to_datetime(df['REF_DATE'])
    df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')
    return df[['REF_DATE', 'GEO', 'VALUE']]


# ════════════════════════════════════════════════════════════════════════════
# PLOT 1 — Alberta Population Growth (line chart)
# ════════════════════════════════════════════════════════════════════════════

def plot_population_growth(df_raw):
    apply_theme()
    alberta = df_raw[
        (df_raw['GEO'] == 'Alberta') &
        (df_raw['REF_DATE'] >= '2012-01-01') &
        (df_raw['REF_DATE'] <= '2025-01-01')
    ].copy().sort_values('REF_DATE')

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(alberta['REF_DATE'], alberta['VALUE'], linewidth=2.5, color=GOLD_2)
    ax.fill_between(alberta['REF_DATE'], alberta['VALUE'], alpha=0.12, color=GOLD_2)

    ax.set_title('Alberta Population Growth (2012–2025)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Population', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.EngFormatter())

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'alberta_population_growth.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/alberta_population_growth.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 2 — Quarterly Growth Rate (bar chart)
# ════════════════════════════════════════════════════════════════════════════

def plot_quarterly_growth_rate(df_raw):
    apply_theme()
    alberta = df_raw[
        (df_raw['GEO'] == 'Alberta') &
        (df_raw['REF_DATE'] >= '2012-01-01') &
        (df_raw['REF_DATE'] <= '2025-01-01')
    ].copy().sort_values('REF_DATE').reset_index(drop=True)
    alberta['Growth_Rate_Pct'] = alberta['VALUE'].pct_change() * 100

    colors = [GOLD_1 if x >= 1.0 else GOLD_DIM
              for x in alberta['Growth_Rate_Pct'].fillna(0)]
    avg = alberta['Growth_Rate_Pct'].mean()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(alberta['REF_DATE'], alberta['Growth_Rate_Pct'],
           width=60, color=colors, edgecolor=BG_FIG, linewidth=0.5)
    ax.axhline(y=0, color=C_EDGE, linewidth=0.8)
    ax.axhline(y=avg, color=GOLD_2, linewidth=2, linestyle='--',
               label=f'Average: {avg:.2f}%')

    ax.set_title('Alberta: Quarterly Population Growth Rate (%)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Growth Rate (%)', fontsize=12)

    leg = ax.legend(fontsize=11)
    style_legend(leg)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'quarterly_growth_rate.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/quarterly_growth_rate.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 3 — Alberta's Share of Canada's Population (area chart)
# ════════════════════════════════════════════════════════════════════════════

def plot_population_share(df_raw):
    apply_theme()
    alberta = df_raw[df_raw['GEO'] == 'Alberta'].copy().sort_values('REF_DATE')
    canada  = df_raw[df_raw['GEO'] == 'Canada'].copy().sort_values('REF_DATE')

    share = alberta.merge(canada, on='REF_DATE', suffixes=('_AB', '_CA'))
    share['AB_Share_Pct'] = (share['VALUE_AB'] / share['VALUE_CA']) * 100

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(share['REF_DATE'], share['AB_Share_Pct'], linewidth=2.5, color=GOLD_2)
    ax.fill_between(share['REF_DATE'], share['AB_Share_Pct'], alpha=0.15, color=GOLD_2)

    ax.set_title("Alberta's Share of Canada's Total Population (%)", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Share (%)', fontsize=12)

    first, last = share.iloc[0], share.iloc[-1]
    ax.annotate(f"{first['AB_Share_Pct']:.1f}%",
                xy=(first['REF_DATE'], first['AB_Share_Pct']),
                fontsize=11, fontweight='bold', color=GOLD_1)
    ax.annotate(f"{last['AB_Share_Pct']:.1f}%",
                xy=(last['REF_DATE'], last['AB_Share_Pct']),
                fontsize=11, fontweight='bold', color=GOLD_1)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'alberta_population_share.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/alberta_population_share.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 4 — Year-over-Year Growth Analysis (dual bar chart)
# ════════════════════════════════════════════════════════════════════════════

def plot_yoy_growth(df_raw):
    apply_theme()
    alberta_all = df_raw[df_raw['GEO'] == 'Alberta'].copy().sort_values('REF_DATE').reset_index(drop=True)

    q1 = alberta_all[alberta_all['REF_DATE'].dt.month == 1].copy().reset_index(drop=True)
    q1['Year'] = q1['REF_DATE'].dt.year
    q1['YoY_Change']     = q1['VALUE'].diff()
    q1['YoY_Growth_Pct'] = q1['VALUE'].pct_change() * 100
    q1 = q1[q1['Year'] >= 1990]

    colors1 = [C_NEG if x < 0 else GOLD_2 for x in q1['YoY_Change'].fillna(0)]
    colors2 = [C_NEG if x < 0 else GOLD_2 for x in q1['YoY_Growth_Pct'].fillna(0)]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    ax1.bar(q1['Year'], q1['YoY_Change'], color=colors1, edgecolor=BG_FIG, linewidth=0.5)
    ax1.set_title('Alberta: Year-over-Year Population Change (Absolute)', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylabel('Population Change', fontsize=12)
    ax1.yaxis.set_major_formatter(mticker.EngFormatter())
    ax1.axhline(y=0, color=C_EDGE, linewidth=0.8)

    ax2.bar(q1['Year'], q1['YoY_Growth_Pct'], color=colors2, edgecolor=BG_FIG, linewidth=0.5)
    ax2.set_title('Alberta: Year-over-Year Population Growth Rate (%)', fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Growth Rate (%)', fontsize=12)
    ax2.axhline(y=0, color=C_EDGE, linewidth=0.8)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'yoy_growth_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/yoy_growth_analysis.png')


# ════════════════════════════════════════════════════════════════════════════
# SHARED — Spending / integration data
# ════════════════════════════════════════════════════════════════════════════

_SPENDING = pd.DataFrame([
    {'Fiscal_Year': '2012-13', 'Year': 2012, 'K12_M': 6179,  'PostSec_M': 2856},
    {'Fiscal_Year': '2013-14', 'Year': 2013, 'K12_M': 6210,  'PostSec_M': 2682},
    {'Fiscal_Year': '2023-24', 'Year': 2023, 'K12_M': 8836,  'PostSec_M': 5604},
    {'Fiscal_Year': '2024-25', 'Year': 2024, 'K12_M': 9252,  'PostSec_M': 6305},
    {'Fiscal_Year': '2025-26', 'Year': 2025, 'K12_M': 9883,  'PostSec_M': 6635},
])
_SPENDING['Total_M'] = _SPENDING['K12_M'] + _SPENDING['PostSec_M']


def build_integrated_df(df_raw):
    pop = df_raw[
        (df_raw['GEO'] == 'Alberta') &
        (df_raw['REF_DATE'].dt.month == 1) &
        (df_raw['REF_DATE'].dt.year.between(2012, 2025))
    ][['REF_DATE', 'VALUE']].copy()
    pop.columns = ['Date', 'Population']
    pop['Year'] = pop['Date'].dt.year
    pop = pop[['Year', 'Population']].reset_index(drop=True)

    df = _SPENDING.merge(pop, on='Year', how='left')
    df['K12_PerCapita']     = (df['K12_M']     * 1_000_000) / df['Population']
    df['PostSec_PerCapita'] = (df['PostSec_M'] * 1_000_000) / df['Population']
    df['Total_PerCapita']   = (df['Total_M']   * 1_000_000) / df['Population']

    base = df.iloc[0]
    df['Pop_Index']     = (df['Population'] / base['Population']) * 100
    df['K12_Index']     = (df['K12_M']      / base['K12_M'])      * 100
    df['PostSec_Index'] = (df['PostSec_M']  / base['PostSec_M'])  * 100
    df['Total_Index']   = (df['Total_M']    / base['Total_M'])    * 100
    return df


# ════════════════════════════════════════════════════════════════════════════
# PLOT 5 — Indexed Growth (population vs spending)
# ════════════════════════════════════════════════════════════════════════════

def plot_integration_indexed(df):
    apply_theme()
    era1 = df[df['Year'].isin([2012, 2013])]
    era2 = df[df['Year'].isin([2023, 2024, 2025])]

    series = [
        ('Pop_Index',     GOLD_1, 'o', 'Population'),
        ('K12_Index',     GOLD_2, 's', 'K-12 Spending'),
        ('PostSec_Index', GOLD_3, '^', 'Post-Secondary Spending'),
        ('Total_Index',   GOLD_4, 'D', 'Total Education Spending'),
    ]

    fig, ax = plt.subplots(figsize=(14, 7))
    for col, color, marker, label in series:
        ax.plot(era1['Year'], era1[col], color=color, linewidth=3,
                marker=marker, markersize=11, zorder=5, label=label)
        ax.plot(era2['Year'], era2[col], color=color, linewidth=3,
                marker=marker, markersize=11, zorder=5)

    ax.axhline(100, color=C_TICK, linewidth=1.2, linestyle='--',
               alpha=0.55, label='2012-13 Baseline (= 100)')
    ax.axvspan(2013.4, 2022.6, alpha=0.05, color=C_TICK, zorder=1)
    ax.text(2018, 109, 'Data gap\n2014 – 2022', ha='center', fontsize=11,
            color=C_TICK, style='italic')

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
        fontsize=18, fontweight='bold', pad=20
    )

    leg = ax.legend(fontsize=12, loc='upper left', framealpha=0.7)
    style_legend(leg)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'integration_indexed_growth.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/integration_indexed_growth.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 6 — Per-Capita Education Spending
# ════════════════════════════════════════════════════════════════════════════

def plot_integration_per_capita(df):
    apply_theme()
    labels = df['Fiscal_Year'].values
    x = np.arange(len(labels))
    w = 0.38

    fig, ax = plt.subplots(figsize=(14, 7))
    bars1 = ax.bar(x - w/2, df['K12_PerCapita'], w, label='K-12',
                   color=GOLD_2, edgecolor=BG_FIG, linewidth=1.5)
    bars2 = ax.bar(x + w/2, df['PostSec_PerCapita'], w, label='Post-Secondary',
                   color=GOLD_3, edgecolor=BG_FIG, linewidth=1.5)

    for bars, color in [(bars1, GOLD_2), (bars2, GOLD_3)]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 18,
                    f'${h:,.0f}', ha='center', va='bottom',
                    fontsize=9, fontweight='bold', color=color)

    gap_y = df['K12_PerCapita'].max() * 0.62
    ax.axvline(1.5, color=C_TICK, linewidth=1.2, linestyle=':', alpha=0.55)
    ax.text(1.5, gap_y, '9-year\ndata gap', ha='center', va='center',
            fontsize=10, color=C_TICK, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_AX,
                      edgecolor=C_EDGE, alpha=0.85))

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
    ax.set_ylabel('Spending per Capita ($)', fontsize=13, labelpad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v:,.0f}'))
    ax.set_title(
        'Alberta: Education Spending per Capita\n'
        'K-12 vs Post-Secondary  |  Nominal figures',
        fontsize=18, fontweight='bold', pad=20
    )

    leg = ax.legend(fontsize=13, loc='upper left', framealpha=0.7)
    style_legend(leg)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'integration_per_capita.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/integration_per_capita.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 7 — Growth Rates Lollipop
# ════════════════════════════════════════════════════════════════════════════

def plot_integration_growth_rates(df):
    apply_theme()
    first, last = df.iloc[0], df.iloc[-1]

    metrics = [
        'Population',
        'K-12 Spending',
        'Post-Secondary\nSpending',
        'Total Education\nSpending',
    ]
    pcts = [
        (last['Population'] / first['Population'] - 1) * 100,
        (last['K12_M']      / first['K12_M']      - 1) * 100,
        (last['PostSec_M']  / first['PostSec_M']  - 1) * 100,
        (last['Total_M']    / first['Total_M']    - 1) * 100,
    ]
    colors = [GOLD_1, GOLD_2, GOLD_3, GOLD_4]

    fig, ax = plt.subplots(figsize=(12, 6))
    y = np.arange(len(metrics))

    for i in range(len(metrics)):
        ax.hlines(y[i], 0, pcts[i], color=colors[i], linewidth=4, alpha=0.85)
        ax.scatter(pcts[i], y[i], color=colors[i], s=280, zorder=5,
                   edgecolor=BG_FIG, linewidth=2)
        ax.text(pcts[i] + 3, y[i], f'+{pcts[i]:.1f}%',
                va='center', fontsize=14, fontweight='bold', color=colors[i])

    pop_pct = pcts[0]
    ax.axvline(pop_pct, color=GOLD_1, linewidth=1.5, linestyle='--', alpha=0.45)
    ax.text(pop_pct + 1, len(metrics) - 0.55,
            f'Population\ngrowth ({pop_pct:.1f}%)',
            color=GOLD_1, fontsize=9, alpha=0.85)

    ax.set_yticks(y)
    ax.set_yticklabels(metrics, fontsize=13, fontweight='bold')
    ax.set_xlabel('Growth from 2012-13 Baseline (%)', fontsize=13, labelpad=10)
    ax.set_xlim(-5, max(pcts) * 1.3)
    ax.set_title(
        'Education Spending vs. Population Growth\n'
        '2012-13 to 2025-26  |  Nominal figures',
        fontsize=18, fontweight='bold', pad=20
    )
    ax.axvline(0, color=C_EDGE, linewidth=1)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'integration_growth_rates.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/integration_growth_rates.png')


# ════════════════════════════════════════════════════════════════════════════
# SHARED — Education spending headline/growth tables
# ════════════════════════════════════════════════════════════════════════════

def build_education_df():
    headline = pd.DataFrame([
        {'Budget_Year': 'Budget 2012', 'Fiscal_Year': '2012-13', 'K-12 ($M)': 6179,  'Post-Secondary ($M)': 2856},
        {'Budget_Year': 'Budget 2013', 'Fiscal_Year': '2013-14', 'K-12 ($M)': 6210,  'Post-Secondary ($M)': 2682},
        {'Budget_Year': 'Budget 2023', 'Fiscal_Year': '2023-24', 'K-12 ($M)': 8836,  'Post-Secondary ($M)': 5604},
        {'Budget_Year': 'Budget 2024', 'Fiscal_Year': '2024-25', 'K-12 ($M)': 9252,  'Post-Secondary ($M)': 6305},
        {'Budget_Year': 'Budget 2025', 'Fiscal_Year': '2025-26', 'K-12 ($M)': 9883,  'Post-Secondary ($M)': 6635},
    ])
    headline['Total ($M)'] = headline['K-12 ($M)'] + headline['Post-Secondary ($M)']

    b2012 = headline[headline['Budget_Year'] == 'Budget 2012'].iloc[0]
    b2025 = headline[headline['Budget_Year'] == 'Budget 2025'].iloc[0]
    growth = pd.DataFrame({
        'Category':         ['K-12', 'Post-Secondary', 'Total Education'],
        'Budget 2012 ($M)': [b2012['K-12 ($M)'], b2012['Post-Secondary ($M)'], b2012['Total ($M)']],
        'Budget 2025 ($M)': [b2025['K-12 ($M)'], b2025['Post-Secondary ($M)'], b2025['Total ($M)']],
    })
    growth['Change ($M)'] = growth['Budget 2025 ($M)'] - growth['Budget 2012 ($M)']
    growth['Change (%)']  = ((growth['Budget 2025 ($M)'] / growth['Budget 2012 ($M)']) - 1) * 100
    return headline, growth


# ════════════════════════════════════════════════════════════════════════════
# PLOT 8 — K-12 vs Post-Secondary Bar Chart
# ════════════════════════════════════════════════════════════════════════════

def plot_infographic_k12_vs_postsec(headline):
    apply_theme()
    plot_df = headline.melt(
        id_vars=['Budget_Year', 'Fiscal_Year'],
        value_vars=['K-12 ($M)', 'Post-Secondary ($M)'],
        var_name='Category', value_name='Spending ($M)'
    )

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(
        data=plot_df, x='Budget_Year', y='Spending ($M)', hue='Category',
        palette=[GOLD_2, GOLD_3], edgecolor=BG_FIG, linewidth=1.5,
        saturation=1.0, ax=ax
    )

    for container in ax.containers:
        for bar in container:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width()/2, h + 100,
                        f'${h:,.0f}M', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color=C_TEXT)

    ax.set_title('Alberta Education Operating Expense\nK-12 vs Post-Secondary (Headline Estimate)',
                 fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('', fontsize=12)
    ax.set_ylabel('Operating Expense ($ millions)', fontsize=13, labelpad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.set_ylim(0, plot_df['Spending ($M)'].max() * 1.18)
    ax.tick_params(axis='x', rotation=15)

    leg = ax.legend(title='Category', fontsize=12, title_fontsize=13,
                    loc='upper left', framealpha=0.7)
    style_legend(leg)
    leg.get_title().set_color(C_TEXT)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'infographic_k12_vs_postsec.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/infographic_k12_vs_postsec.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 9 — Stacked Horizontal Bar
# ════════════════════════════════════════════════════════════════════════════

def plot_infographic_total_stacked(headline):
    apply_theme()
    budgets = headline['Budget_Year'].values
    k12     = headline['K-12 ($M)'].values
    ps      = headline['Post-Secondary ($M)'].values
    y_pos   = np.arange(len(budgets))

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.barh(y_pos, k12, height=0.55, label='K-12',
            color=GOLD_2, edgecolor=BG_FIG, linewidth=1.2)
    ax.barh(y_pos, ps, height=0.55, left=k12, label='Post-Secondary',
            color=GOLD_3, edgecolor=BG_FIG, linewidth=1.2)

    for i in range(len(budgets)):
        ax.text(k12[i]/2, y_pos[i], f'${k12[i]:,.0f}M',
                ha='center', va='center', fontsize=10, fontweight='bold', color=BG_FIG)
        ax.text(k12[i] + ps[i]/2, y_pos[i], f'${ps[i]:,.0f}M',
                ha='center', va='center', fontsize=10, fontweight='bold', color=BG_FIG)
        total = k12[i] + ps[i]
        ax.text(total + 150, y_pos[i], f'Total: ${total:,.0f}M',
                ha='left', va='center', fontsize=11, fontweight='bold', color=GOLD_1)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(budgets, fontsize=13, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('Operating Expense ($ millions)', fontsize=13, labelpad=10)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.set_title('Total Education Spending by Budget Year\n(K-12 + Post-Secondary)',
                 fontsize=18, fontweight='bold', pad=20)

    leg = ax.legend(fontsize=12, loc='lower right', framealpha=0.7)
    style_legend(leg)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'infographic_total_stacked.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/infographic_total_stacked.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 10 — 2012 vs 2025 Growth Comparison
# ════════════════════════════════════════════════════════════════════════════

def plot_infographic_growth_comparison(headline, growth):
    apply_theme()
    categories = growth['Category'].values
    vals_2012  = growth['Budget 2012 ($M)'].values
    vals_2025  = growth['Budget 2025 ($M)'].values
    change_pct = growth['Change (%)'].values
    x = np.arange(len(categories))
    width = 0.32

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(x - width/2, vals_2012, width, label='Budget 2012 (2012-13)',
           color=GOLD_DIM, edgecolor=BG_FIG, linewidth=1.5)
    ax.bar(x + width/2, vals_2025, width, label='Budget 2025 (2025-26)',
           color=GOLD_1, edgecolor=BG_FIG, linewidth=1.5)

    for i in range(len(categories)):
        ax.text(x[i] - width/2, vals_2012[i] + 150,
                f'${vals_2012[i]:,.0f}M', ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=GOLD_DIM)
        ax.text(x[i] + width/2, vals_2025[i] + 150,
                f'${vals_2025[i]:,.0f}M', ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=GOLD_1)
        mid_y = max(vals_2012[i], vals_2025[i]) + 800
        ax.annotate(f'+{change_pct[i]:.0f}%',
                    xy=(x[i], mid_y), fontsize=16, fontweight='bold',
                    ha='center', va='bottom', color=GOLD_2,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=BG_AX,
                              edgecolor=GOLD_2, alpha=0.9))

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=14, fontweight='bold')
    ax.set_ylabel('Operating Expense ($ millions)', fontsize=13, labelpad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.set_ylim(0, max(vals_2025) * 1.35)
    ax.set_title('Education Spending Growth: 2012 → 2025\n13 Years of Change',
                 fontsize=18, fontweight='bold', pad=20)

    leg = ax.legend(fontsize=13, loc='upper left', framealpha=0.7)
    style_legend(leg)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'infographic_growth_2012_vs_2025.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/infographic_growth_2012_vs_2025.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 11 — Donut Charts (budget composition)
# ════════════════════════════════════════════════════════════════════════════

def plot_infographic_donut_composition(headline):
    apply_theme()
    fig, axes = plt.subplots(1, 5, figsize=(22, 5))
    fig.suptitle('K-12 vs Post-Secondary Share by Budget Year',
                 fontsize=18, fontweight='bold', y=1.05)

    for ax, (_, row) in zip(axes, headline.iterrows()):
        vals  = [row['K-12 ($M)'], row['Post-Secondary ($M)']]
        total = sum(vals)
        pcts  = [v / total * 100 for v in vals]

        ax.pie(
            vals, colors=[GOLD_2, GOLD_3], startangle=90,
            wedgeprops=dict(width=0.4, edgecolor=BG_FIG, linewidth=2)
        )
        ax.text(0,  0.08, f'${total:,.0f}M', ha='center', va='center',
                fontsize=12, fontweight='bold', color=C_TEXT)
        ax.text(0, -0.12, 'Total', ha='center', va='center',
                fontsize=9, color=C_TICK)
        ax.set_title(row['Budget_Year'], fontsize=12, fontweight='bold',
                     color=BUDGET_YEAR_PALETTE.get(row['Budget_Year'], C_TEXT), pad=12)
        ax.text(0, -0.65,
                f'K-12: {pcts[0]:.0f}%  |  Post-Sec: {pcts[1]:.0f}%',
                ha='center', va='center', fontsize=8, color=C_TICK)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'infographic_donut_composition.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/infographic_donut_composition.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 12 — Heatmap
# ════════════════════════════════════════════════════════════════════════════

def plot_infographic_heatmap(headline):
    apply_theme()
    heat_data = headline.set_index('Budget_Year')[['K-12 ($M)', 'Post-Secondary ($M)', 'Total ($M)']]

    gold_cmap = mcolors.LinearSegmentedColormap.from_list(
        'gold_dark', [BG_AX, GOLD_DIM, GOLD_2, GOLD_1], N=256
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(
        heat_data, annot=True, fmt=',.0f', cmap=gold_cmap,
        linewidths=2, linecolor=BG_FIG,
        cbar_kws={'label': '$ millions'},
        annot_kws={'fontsize': 13, 'fontweight': 'bold', 'color': C_TEXT},
        ax=ax
    )

    ax.set_title('Education Spending Heatmap\n(Higher = More Spending)',
                 fontsize=16, fontweight='bold', pad=15)
    ax.set_ylabel('')
    ax.tick_params(axis='y', rotation=0)
    ax.tick_params(axis='x', rotation=15)

    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.label.set_color(C_TEXT)
    cbar.ax.tick_params(colors=C_TICK)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'infographic_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/infographic_heatmap.png')


# ════════════════════════════════════════════════════════════════════════════
# PLOT 13 — Lollipop Growth Chart
# ════════════════════════════════════════════════════════════════════════════

def plot_infographic_lollipop(growth):
    apply_theme()
    categories = growth['Category'].values
    pcts   = growth['Change (%)'].values
    colors = [GOLD_2, GOLD_3, GOLD_1]
    y_pos  = np.arange(len(categories))

    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(len(categories)):
        ax.hlines(y=y_pos[i], xmin=0, xmax=pcts[i],
                  color=colors[i], linewidth=3, alpha=0.8)
        ax.scatter(pcts[i], y_pos[i], color=colors[i],
                   s=250, zorder=5, edgecolor=BG_FIG, linewidth=2)
        ax.text(pcts[i] + 3, y_pos[i],
                f'+{pcts[i]:.0f}%  (+${growth["Change ($M)"].iloc[i]:,.0f}M)',
                va='center', fontsize=13, fontweight='bold', color=colors[i])

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=14, fontweight='bold')
    ax.set_xlabel('Growth (%)', fontsize=13, labelpad=10)
    ax.set_xlim(-5, max(pcts) * 1.4)
    ax.set_title('Education Spending Growth 2012 → 2025\nPercentage Increase by Category',
                 fontsize=16, fontweight='bold', pad=15)
    ax.axvline(x=0, color=C_EDGE, linewidth=1)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / 'infographic_lollipop_growth.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('Saved -> plots/infographic_lollipop_growth.png')


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    PLOTS_DIR.mkdir(exist_ok=True)

    print('Loading population data...')
    df_raw = load_population()

    print('\n--- Population charts ---')
    plot_population_growth(df_raw)
    plot_quarterly_growth_rate(df_raw)
    plot_population_share(df_raw)
    plot_yoy_growth(df_raw)

    print('\n--- Integration charts (population vs spending) ---')
    df_int = build_integrated_df(df_raw)
    plot_integration_indexed(df_int)
    plot_integration_per_capita(df_int)
    plot_integration_growth_rates(df_int)

    print('\n--- Education infographic charts ---')
    headline, growth = build_education_df()
    plot_infographic_k12_vs_postsec(headline)
    plot_infographic_total_stacked(headline)
    plot_infographic_growth_comparison(headline, growth)
    plot_infographic_donut_composition(headline)
    plot_infographic_heatmap(headline)
    plot_infographic_lollipop(growth)

    print('\nAll 13 plots regenerated with the Dark Grey + Gold theme.')
    print('Output directory: ' + str(PLOTS_DIR))
