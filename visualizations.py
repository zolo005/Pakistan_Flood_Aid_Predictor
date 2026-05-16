import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ══════════════════════════════════════════════════════════════
# GLOBAL STYLE — matches app.py dark theme
# ══════════════════════════════════════════════════════════════
DARK_BG     = '#05111f'
CARD_BG     = '#0d2035'
TEAL        = '#00d4b8'
AMBER       = '#f5a623'
RED         = '#f04040'
GREEN       = '#10c97a'
MUTED       = '#6b8aaa'
TEXT        = '#dce8f5'
GRID        = '#0f2540'

PROVINCE_COLORS = {
    'Sindh':            '#f04040',
    'Balochistan':      '#f5a623',
    'KPK':              '#00d4b8',
    'Punjab':           '#a78bfa',
    'Gilgit_Baltistan': '#10c97a',
}

def style_axis(ax, title='', xlabel='', ylabel=''):
    """Apply consistent dark professional styling to any axis."""
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.spines['bottom'].set_color(GRID)
    ax.spines['left'].set_color(GRID)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.set_xlabel(xlabel, fontsize=10, labelpad=8)
    ax.set_ylabel(ylabel, fontsize=10, labelpad=8)
    ax.yaxis.set_tick_params(labelcolor=MUTED)
    ax.xaxis.set_tick_params(labelcolor=MUTED)
    if title:
        ax.set_title(title, fontsize=13, fontweight='bold',
                     color=TEXT, pad=14, loc='left')


def make_fig(w=11, h=4.5):
    """Create a dark-background figure."""
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    return fig, ax


def show_visualizations():
    df = pd.read_csv('flood_data.csv')

    st.markdown("---")

    # ── section header ────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.5rem;
                font-weight:800;color:#dce8f5;letter-spacing:2px;
                border-left:4px solid #00d4b8;padding-left:14px;margin-bottom:20px">
        📊 PAKISTAN 2022 FLOOD DATA INSIGHTS
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # ROW 1 — Bar chart + Horizontal bar chart side by side
    # ══════════════════════════════════════════════════════════
    r1c1, r1c2 = st.columns(2)

    # ── Chart 1: Aid needed by province ──────────────────────
    with r1c1:
        aid_by_province = (df.groupby('province')['aid_needed']
                             .sum()
                             .sort_values(ascending=False))
        provinces = aid_by_province.index.tolist()
        colors    = [PROVINCE_COLORS.get(p, TEAL) for p in provinces]

        fig1, ax1 = make_fig(6, 4.5)
        bars = ax1.bar(provinces, aid_by_province.values,
                       color=colors, width=0.55, zorder=3,
                       edgecolor='none')
        ax1.set_axisbelow(True)
        ax1.yaxis.grid(True, color=GRID, linewidth=0.6, linestyle='--')
        style_axis(ax1,
                   title='Households Requiring Aid by Province',
                   xlabel='Province',
                   ylabel='Households')
        for bar, val in zip(bars, aid_by_province.values):
            ax1.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + max(aid_by_province.values) * 0.02,
                     f'{int(val):,}',
                     ha='center', va='bottom',
                     color=TEXT, fontsize=8.5, fontweight='bold')
        ax1.set_xticklabels(provinces, rotation=15, ha='right', fontsize=8.5)
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    # ── Chart 2: Average income by province ──────────────────
    with r1c2:
        avg_income = (df.groupby('province')['monthly_income_pkr']
                        .mean()
                        .sort_values())
        prov_list  = avg_income.index.tolist()
        bar_colors = [PROVINCE_COLORS.get(p, TEAL) for p in prov_list]

        fig2, ax2 = make_fig(6, 4.5)
        hbars = ax2.barh(prov_list, avg_income.values,
                         color=bar_colors, height=0.5,
                         edgecolor='none', zorder=3)
        ax2.set_axisbelow(True)
        ax2.xaxis.grid(True, color=GRID, linewidth=0.6, linestyle='--')
        style_axis(ax2,
                   title='Avg Monthly Income by Province',
                   xlabel='PKR',
                   ylabel='')
        for bar, val in zip(hbars, avg_income.values):
            ax2.text(val + avg_income.max() * 0.02,
                     bar.get_y() + bar.get_height() / 2,
                     f'PKR {val:,.0f}',
                     va='center', color=TEXT, fontsize=8, fontweight='bold')
        ax2.set_yticklabels(prov_list, fontsize=8.5)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # ══════════════════════════════════════════════════════════
    # ROW 2 — Flood risk line chart + Pie chart side by side
    # ══════════════════════════════════════════════════════════
    r2c1, r2c2 = st.columns([3, 2])

    # ── Chart 3: Flood risk distribution (line chart) ────────
    with r2c1:
        fig3, ax3 = make_fig(7, 4.2)
        for province in df['province'].unique():
            pdata  = df[df['province'] == province]['flood_risk_level']
            counts, edges = np.histogram(pdata, bins=10, range=(1, 10))
            centers = (edges[:-1] + edges[1:]) / 2
            color   = PROVINCE_COLORS.get(province, TEAL)
            ax3.plot(centers, counts,
                     color=color, linewidth=2,
                     label=province, marker='o',
                     markersize=4, zorder=3)
            ax3.fill_between(centers, counts,
                             alpha=0.08, color=color)
        ax3.set_axisbelow(True)
        ax3.yaxis.grid(True, color=GRID, linewidth=0.6, linestyle='--')
        style_axis(ax3,
                   title='Flood Risk Distribution by Province',
                   xlabel='Flood Risk Level (1=Low → 10=High)',
                   ylabel='Households')
        legend = ax3.legend(fontsize=8, framealpha=0,
                            labelcolor=TEXT, loc='upper right')
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

    # ── Chart 4: Aid vs No Aid donut chart ───────────────────
    with r2c2:
        aid_counts = df['aid_needed'].value_counts()
        labels     = ['Aid Required', 'No Aid Required']
        sizes      = [aid_counts.get(1, 0), aid_counts.get(0, 0)]
        clrs       = [RED, GREEN]

        fig4, ax4 = make_fig(5, 4.2)
        wedges, texts, autotexts = ax4.pie(
            sizes,
            labels=None,
            colors=clrs,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.78,
            wedgeprops=dict(width=0.52, edgecolor=DARK_BG, linewidth=2)
        )
        for at in autotexts:
            at.set_color(TEXT)
            at.set_fontsize(10)
            at.set_fontweight('bold')

        # centre label
        ax4.text(0, 0, f"{int(sum(sizes)):,}\nHouseholds",
                 ha='center', va='center',
                 color=TEXT, fontsize=9, fontweight='bold')

        legend_patches = [
            mpatches.Patch(color=RED,   label=f'Aid Required  ({sizes[0]:,})'),
            mpatches.Patch(color=GREEN, label=f'Not Required  ({sizes[1]:,})'),
        ]
        ax4.legend(handles=legend_patches, loc='lower center',
                   bbox_to_anchor=(0.5, -0.08),
                   framealpha=0, labelcolor=TEXT, fontsize=8.5)
        ax4.set_title('Overall Aid Requirement',
                      fontsize=13, fontweight='bold',
                      color=TEXT, pad=14, loc='left')
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

    # ══════════════════════════════════════════════════════════
    # ROW 3 — Family size vs Aid stacked bar
    # ══════════════════════════════════════════════════════════
    fig5, ax5 = make_fig(11, 4)
    df['family_size_group'] = pd.cut(
        df['family_size'],
        bins=[0, 3, 5, 8, 15],
        labels=['1–3', '4–5', '6–8', '9+']
    )
    grp = (df.groupby(['family_size_group', 'aid_needed'], observed=True)
             .size()
             .unstack(fill_value=0))

    x      = np.arange(len(grp.index))
    width  = 0.35
    b1 = ax5.bar(x - width/2,
                 grp.get(0, pd.Series([0]*len(grp))),
                 width, label='No Aid Required',
                 color=GREEN, edgecolor='none', zorder=3)
    b2 = ax5.bar(x + width/2,
                 grp.get(1, pd.Series([0]*len(grp))),
                 width, label='Aid Required',
                 color=RED, edgecolor='none', zorder=3)
    ax5.set_axisbelow(True)
    ax5.yaxis.grid(True, color=GRID, linewidth=0.6, linestyle='--')
    ax5.set_xticks(x)
    ax5.set_xticklabels(grp.index, fontsize=9)
    style_axis(ax5,
               title='Aid Requirement by Family Size Group',
               xlabel='Family Size',
               ylabel='Number of Households')
    legend5 = ax5.legend(fontsize=9, framealpha=0, labelcolor=TEXT)
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

    # ══════════════════════════════════════════════════════════
    # REAL STATISTICS FOOTER
    # ══════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Barlow Condensed',sans-serif;font-size:1rem;
                font-weight:700;color:#00d4b8;text-transform:uppercase;
                letter-spacing:2px;border-left:3px solid #00d4b8;
                padding-left:10px;margin-bottom:16px">
        📋 Real 2022 Pakistan Flood Statistics
    </div>
    """, unsafe_allow_html=True)

    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    mc1.metric("People Affected",   "33 Million")
    mc2.metric("Houses Damaged",    "1.7 Million")
    mc3.metric("Districts Affected","116")
    mc4.metric("Provinces Affected","5")
    mc5.metric("Economic Loss",     "$30 Billion")
    st.caption("Source: OCHA Pakistan Flood Response 2022 | World Bank Pakistan Floods Assessment")