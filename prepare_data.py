import pandas as pd
import numpy as np

np.random.seed(42)

# ── Load real data ──────────────────────────────────────────
df_r6 = pd.read_excel('pak_dtm_flood_response_cni_r6_hdx.xlsx', sheet_name='Data')
df_r7 = pd.read_excel('pak_dtm_flood_response_cnit_r7_for-publishing_final_ya.xlsx')

# ── Clean r6 (KPK + Balochistan) ───────────────────────────
df_r6 = df_r6[df_r6['Province'].isin(['Khyber Pakhtunkhwa', 'Balochistan'])]
df_r6 = df_r6.rename(columns={
    'Province': 'province',
    'District': 'district',
    'C.1 What is the estimated total population in this location? \u2013 individuals': 'total_population',
    'C.2 What is the estimated number of households in this location? - households': 'total_households',
    'Total TDP Individuals': 'displaced_individuals',
    'Total TDP Households': 'displaced_households',
})
df_r6 = df_r6[['province', 'district', 'total_population',
                'total_households', 'displaced_individuals', 'displaced_households']]
df_r6 = df_r6.dropna(subset=['province', 'district'])
df_r6 = df_r6.fillna(0)

# ── Clean r7 (Punjab) ──────────────────────────────────────
df_r7 = df_r7.rename(columns={
    'Province': 'province',
    'District': 'district',
    'C.1 What is the current estimated total population in this location? \u2013 individuals': 'total_population',
    'C.2 What is the current estimated number of households in this location? - households': 'total_households',
    'C.3 What is the estimated no. of TDPs who belong to this village and are displaced inside this village? (During the current 2025 monsoon season) \u2013 individuals': 'displaced_individuals',
    'C.4 What is the estimated no. of TDP households who belong to this village and are displaced inside this village? (During the current 2025 monsoon season) \u2013 households': 'displaced_households',
})
df_r7 = df_r7[['province', 'district', 'total_population',
                'total_households', 'displaced_individuals', 'displaced_households']]
df_r7 = df_r7.dropna(subset=['province', 'district'])
df_r7 = df_r7.fillna(0)

# ── Combine real data ───────────────────────────────────────
df_real = pd.concat([df_r6, df_r7], ignore_index=True)
df_real['province'] = df_real['province'].replace({'Khyber Pakhtunkhwa': 'KPK'})

print(f"Real data rows: {len(df_real)}")
print(f"Province breakdown:\n{df_real['province'].value_counts()}")

# ── Add synthetic columns to real data ─────────────────────
n_real = len(df_real)
df_real['monthly_income_pkr'] = np.where(
    df_real['province'] == 'Balochistan',
    np.random.normal(10000, 3000, n_real).astype(int).clip(3000, 80000),
    np.where(df_real['province'] == 'KPK',
             np.random.normal(15000, 3000, n_real).astype(int).clip(3000, 80000),
             np.random.normal(20000, 4000, n_real).astype(int).clip(3000, 80000))
)
df_real['family_size'] = np.random.randint(3, 12, n_real)
df_real['house_condition'] = np.random.randint(1, 5, n_real)
df_real['distance_from_relief_center_km'] = np.random.randint(1, 100, n_real)
df_real['previous_flood_damage'] = np.random.choice([0, 1], n_real, p=[0.3, 0.7])
df_real['access_to_clean_water'] = np.random.choice([0, 1], n_real, p=[0.6, 0.4])
df_real['livestock_lost'] = np.random.choice([0, 1], n_real, p=[0.4, 0.6])
df_real['crops_damaged'] = np.random.choice([0, 1], n_real, p=[0.4, 0.6])
df_real['children_under_age_5'] = np.random.choice([0, 1], n_real)
df_real['disabled_family_members'] = np.random.choice([0, 1], n_real, p=[0.8, 0.2])
# Flood risk from displacement ratio
df_real['total_population'] = pd.to_numeric(df_real['total_population'], errors='coerce').fillna(1)
df_real['displaced_individuals'] = pd.to_numeric(df_real['displaced_individuals'], errors='coerce').fillna(0)
df_real['displacement_ratio'] = (
    df_real['displaced_individuals'] / df_real['total_population'].replace(0, 1)
).clip(0, 1)
df_real['flood_risk_level'] = (df_real['displacement_ratio'] * 9 + 1).astype(int).clip(1, 10)

# ── Synthetic Sindh + Gilgit Baltistan ─────────────────────
sindh_districts = ['Dadu', 'Jacobabad', 'Kambar', 'Khairpur', 'Mirpur Khas',
                   'Jamshoro', 'Sanghar', 'Badin', 'Sukkur', 'Larkana']
gb_districts = ['Ghizer', 'Nagar', 'Diamer', 'Ghanche', 'Astore',
                'Gilgit', 'Hunza', 'Skardu', 'Shigar', 'Kharmang']

def make_synthetic(province, districts, n, avg_income, flood_weight):
    return pd.DataFrame({
        'province': province,
        'district': np.random.choice(districts, n),
        'total_population': np.random.randint(500, 10000, n),
        'total_households': np.random.randint(50, 1000, n),
        'displaced_individuals': np.random.randint(0, 500, n),
        'displaced_households': np.random.randint(0, 100, n),
        'monthly_income_pkr': np.random.normal(avg_income, 3000, n).astype(int).clip(3000, 80000),
        'family_size': np.random.randint(3, 12, n),
        'house_condition': np.random.randint(1, 5, n),
        'distance_from_relief_center_km': np.random.randint(1, 100, n),
        'previous_flood_damage': np.random.choice([0, 1], n, p=[0.3, 0.7]),
        'access_to_clean_water': np.random.choice([0, 1], n, p=[0.6, 0.4]),
        'livestock_lost': np.random.choice([0, 1], n, p=[0.4, 0.6]),
        'crops_damaged': np.random.choice([0, 1], n, p=[0.4, 0.6]),
        'flood_risk_level': np.clip(np.random.normal(flood_weight * 10, 1.5, n).astype(int), 1, 10),
        'displacement_ratio': np.random.uniform(0, 0.5, n),
        'children_under_age_5': np.random.randint(0, 5, n),
        'disabled_family_members': np.random.choice([0, 1], n, p=[0.8, 0.2])
    })

df_sindh = make_synthetic('Sindh', sindh_districts, 1000, 12000, 0.9)
df_gb = make_synthetic('Gilgit_Baltistan', gb_districts, 500, 13000, 0.6)

# ── Final dataset ───────────────────────────────────────────
df_final = pd.concat([df_real, df_sindh, df_gb], ignore_index=True)

# Aid needed logic
df_final['aid_needed'] = (
    (df_final['monthly_income_pkr'] < 20000) &
    (df_final['flood_risk_level'] >= 6) |
    (df_final['disabled_family_members'] == 1) &
    (df_final['flood_risk_level'] >= 5) &
    (df_final['monthly_income_pkr'] < 25000) |
    (df_final['children_under_age_5'] >= 3) &
    (df_final['flood_risk_level'] >= 5)
).astype(int)

# Add noise
noise_idx = df_final.sample(frac=0.025, random_state=42).index
df_final.loc[noise_idx, 'aid_needed'] = 1 - df_final.loc[noise_idx, 'aid_needed']

# ── Save ────────────────────────────────────────────────────
df_final.to_csv('flood_data.csv', index=False)
print("\n✅ Final dataset created successfully!")
print(f"Total records: {len(df_final)}")
print(f"Aid needed: {df_final['aid_needed'].sum()} households")
print(f"\nFinal province breakdown:\n{df_final['province'].value_counts()}")