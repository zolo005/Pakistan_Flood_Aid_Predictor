# 🌊 Pakistan Flood Aid Predictor

A humanitarian relief distribution system built to predict which households need urgent flood aid during Pakistan's catastrophic 2022 floods.

---
## 📖 About The Project
In 2022, Pakistan experienced its worst floods in recorded history, affecting over 33 million people, damaging 1.7 million homes, and devastating 116 districts across 5 provinces. Growing up in Dadu/Sindh, one of the most severely affected regions. I witnessed firsthand how families were left without aid not because resources didn't exist, but because there was no data-driven system to identify who needed help most urgently.

This project is my attempt to solve that problem using Machine Learning and Data Science.

The system takes household-level information as input and predicts whether a family requires flood relief aid. When aid is required, it identifies the nearest official relief center and automatically dispatches a structured email notification, turning a prediction into an actionable relief request.

---
## ✨ Features
- **ML-Powered Prediction** - Random Forest Classifier trained on 14,320 households across 5 provinces
- **Real Data** - Built using official IOM DTM Pakistan Flood Response 2022 data from OCHA HDX
- **Province → District → City** - Three-level location selection covering all major flood-affected areas
- **Nearby Relief Centers** - Automatically shows PDMA, Red Crescent and Edhi Foundation centers for selected district
- **Professional UI** - Dark humanitarian dashboard design built with Streamlit
- **Relief Dispatch** - When aid is required, collects applicant details and emails the nearest relief center automatically
- **CSV Logging** - Every submission logged locally for record keeping
- **Severity Classification** - Critical, High and Moderate priority tags based on confidence score

---
## 📊 Model Details
| Property | Value |
|----------|-------|
| Algorithm | Random Forest Classifier |
| Training Data | 14,320 households |
| Accuracy | 87.36% |
| Data Source | IOM DTM Pakistan Flood Response 2022 — OCHA HDX |
| Provinces Covered | Sindh, Balochistan, KPK, Punjab, Gilgit-Baltistan |

---
### Input Features
- Province, District, City
- Monthly Income (PKR)
- Family Size
- Children Under Age 5
- Elderly Members (60+)
- Flood Risk Level (Low / Medium / High)
- House Condition (Poor / Fair / Good / Excellent)
- Distance from Relief Center (km)
- Previous Flood Damage
- Access to Clean Water
- Livestock Lost
- Crops Damaged
- Disabled Family Members
- Medical Emergency in Household

---
## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| Python | Core language |
| scikit-learn | ML model training and prediction |
| pandas | Data manipulation and processing |
| numpy | Numerical operations and dataset generation |
| Streamlit | Web interface and deployment |
| matplotlib | Data visualizations |
| seaborn | Statistical charts |
| pickle | Model serialization |
| smtplib | Automated email dispatch |


---
## 📁 Project Structure
Pakistan_Flood_Aid_Predictor/
│
├── app.py                  # Main Streamlit web application
├── model.py                # ML model training script
├── prepare_data.py         # Dataset preparation from real IOM data
├── visualizations.py       # Data visualization charts
├── flood_model.pkl         # Trained Random Forest model
├── flood_data.csv          # Processed dataset
├── submissions_log.csv     # Auto-generated submission records
│
├── pak_dtm_flood_response_cni_r6_hdx.xlsx
└── pak_dtm_flood_response_cnit_r7_for-publishing_final_ya.xlsx


---
## 🚀 How To Run
**1. Clone the repository**
```bash
git clone https://github.com/zolo005/Pakistan_Flood_Aid_Predictor.git
cd Pakistan_Flood_Aid_Predictor
```

**2. Install dependencies**
```bash
pip install pandas numpy scikit-learn streamlit matplotlib seaborn openpyxl
```

**3. Prepare the dataset**
```bash
python prepare_data.py
```

**4. Train the model**
```bash
python model.py
```

**5. Run the app**
```bash
streamlit run app.py
```

---
## 📧 Email Configuration
To enable automated email dispatch to relief centers, open `app.py` and replace:
```python
SENDER_EMAIL    = "your_gmail@gmail.com"
SENDER_PASSWORD = "your_app_password"
```
Use a Gmail App Password — not your regular password.
To generate one: Google Account → Security → 2-Step Verification → App Passwords

---
## 📦 Data Sources
- **IOM DTM Pakistan Flood Response 2022** Round 6 & 7, OCHA Humanitarian Data Exchange (HDX)
- **Sindh & Gilgit-Baltistan** Synthetically generated based on real OCHA 2022 flood statistics
- **Relief Center Data** PDMA, Pakistan Red Crescent, Edhi Foundation official contact information

---
## 👨‍💻 About The Developer
Built by **Awais Ali Abro** a Data Science student from Dadu, Sindh, Pakistan.
This project was built entirely through self-study alongside FSC Pre-Engineering studies. The motivation came from personally witnessing the 2022 floods devastate my community in Dadu,Sindh and seeing families struggle to access aid because of poor data systems.
Certifications: Oracle AI Foundations Associate & Oracle Generative AI Professional

---
## 📄 License
This project is open source and available for humanitarian and educational use.
---
*Built with the goal of making data science useful for the people who need it most.*