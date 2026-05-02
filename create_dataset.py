import pandas as pd
import numpy as np

np.random.seed(42)

province_data = {
    'Sindh': {
        'districts': ['Dadu', 'Jacobabad', 'Kambar', 'Khairpur', 'Mirpur Khas',
                      'Jamshoro', 'Sanghar', 'Badin', 'Sukkur', 'Larkana'],
        'flood_risk_weight': 0.9,
        'avg_income': 12000,
        'houses_damaged': 57496
    },
    'Balochistan': {
        'districts': ['Quetta', 'Kharan', 'Washuk', 'Jaffarabad', 'Jhal Magsi',
                      'Sohbatpur', 'Naseerabad', 'Lasbela', 'Kech', 'Panjgur'],
        'flood_risk_weight': 0.8,
        'avg_income': 10000,
        'houses_damaged': 426897
    },
    'KPK': {
        'districts': ['Swat', 'Nowshera', 'Charsadda', 'Peshawar', 'DI Khan',
                      'Lower Dir', 'Upper Dir', 'Chitral', 'Kohistan', 'Buner'],
        'flood_risk_weight': 0.7,
        'avg_income': 15000,
        'houses_damaged': 326897
    },
    'Punjab': {
        'districts': ['Taunsa', 'Dera Ghazi Khan', 'Rajanpur', 'Muzaffargarh',
                      'Layyah', 'Bhakkar', 'Mianwali', 'Bahawalpur', 'RY Khan', 'Multan'],
        'flood_risk_weight': 0.5,
        'avg_income': 20000,
        'houses_damaged': 3858
    },
    'Gilgit_Baltistan': {
        'districts': ['Ghizer', 'Nagar', 'Diamer','Ghanche', 'Astore',
                      'Gilgit', 'Hunza', 'Skardu', 'Shigar', 'Kharmang'],
        'flood_risk_weight': 0.6,
        'avg_income': 13000,
        'houses_damaged': 1160
    }
}

records = []
for province, info in province_data.items():
    n = 100
    for _ in range(n):
        district = np.random.choice(info['districts'])
        income = int(np.random.normal(info['avg_income'], 4000))
        income = max(3000, min(80000, income))
        flood_risk = int(np.random.normal(info['flood_risk_weight'] * 10, 1.5))
        flood_risk = max(1, min(10, flood_risk))

        record = {
            'province': province,
            'district': district,
            'monthly_income_pkr': income,
            'family_size': np.random.randint(3, 12),
            'flood_risk_level': flood_risk,
            'house_condition': np.random.randint(1, 5),
            'distance_from_relief_center_km': np.random.randint(1, 100),
            'previous_flood_damage': np.random.choice([0, 1], p=[0.3, 0.7]),
            'access_to_clean_water': np.random.choice([0, 1], p=[0.6, 0.4]),
            'livestock_lost': np.random.choice([0, 1], p=[0.4, 0.6]),
            'crops_damaged': np.random.choice([0, 1], p=[0.4, 0.6]),
        }
        records.append(record)

df = pd.DataFrame(records)

df['aid_needed'] = (
    (df['monthly_income_pkr'] < 20000) &
    (df['flood_risk_level'] >= 6)
).astype(int)

# Add realistic noise - real world data is never perfect
noise_idx = df.sample(frac=0.09, random_state=42).index
df.loc[noise_idx, 'aid_needed'] = 1 - df.loc[noise_idx, 'aid_needed']

df.to_csv('flood_data.csv', index=False)
print("✅ Real-based dataset created successfully!")
print(f"Total records: {len(df)}")
print(f"Aid needed: {df['aid_needed'].sum()} households")
print(f"\nProvince breakdown:\n{df['province'].value_counts()}")
print(f"\nSample data:\n{df.head()}")