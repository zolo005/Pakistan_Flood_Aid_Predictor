import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_visualizations():
    df = pd.read_csv('flood_data.csv')

    st.markdown("---")
    st.header("📊 Pakistan 2022 Flood Data Insights")

    # Chart 1 - Aid needed by province
    st.subheader("🏠 Households Needing Aid by Province")
    aid_by_province = df.groupby('province')['aid_needed'].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    colors = ['#FF4B4B', '#FF8C00', '#FFC300', '#4CAF50', '#2196F3']
    ax1.bar(aid_by_province.index, aid_by_province.values, color=colors)
    ax1.set_title('Households Requiring Aid by Province', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Province')
    ax1.set_ylabel('Number of Households')
    for i, v in enumerate(aid_by_province.values):
        ax1.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    st.pyplot(fig1)

    # Chart 2 - Average income by province
    st.subheader("💰 Average Monthly Income by Province (PKR)")
    avg_income = df.groupby('province')['monthly_income_pkr'].mean().sort_values()
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.barh(avg_income.index, avg_income.values, color='#2196F3')
    ax2.set_title('Average Monthly Income by Province', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Average Income (PKR)')
    for i, v in enumerate(avg_income.values):
        ax2.text(v + 100, i, f'PKR {v:,.0f}', va='center', fontweight='bold')
    st.pyplot(fig2)

    # Chart 3 - Flood risk distribution
    st.subheader("🌊 Flood Risk Level Distribution by Province")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    for province in df['province'].unique():
        province_data = df[df['province'] == province]['flood_risk_level']
        ax3.hist(province_data, alpha=0.5, label=province, bins=10)
    ax3.set_title('Flood Risk Distribution by Province', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Flood Risk Level')
    ax3.set_ylabel('Number of Households')
    ax3.legend()
    st.pyplot(fig3)

    # Chart 4 - Aid vs No Aid pie chart
    st.subheader("📈 Overall Aid Requirement")
    aid_counts = df['aid_needed'].value_counts()
    fig4, ax4 = plt.subplots(figsize=(7, 7))
    ax4.pie(aid_counts.values,
            labels=['Aid Required', 'No Aid Required'],
            colors=['#FF4B4B', '#4CAF50'],
            autopct='%1.1f%%',
            startangle=90)
    ax4.set_title('Overall Aid Requirement Distribution', fontsize=14, fontweight='bold')
    st.pyplot(fig4)

    # Real statistics footer
    st.markdown("---")
    st.subheader("📋 Real 2022 Pakistan Flood Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("People Affected", "33 Million")
    col2.metric("Houses Damaged", "1.7 Million")
    col3.metric("Districts Affected", "116")
    col4.metric("Provinces Affected", "5")
    st.caption("Source: OCHA Pakistan Flood Response 2022")