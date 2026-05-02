import streamlit as st
import pandas as pd
import numpy as np
import pickle
import smtplib
import os
import csv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from visualizations import show_visualizations


# EMAIL CONFIG (need to be replaced with real gmail and pass)
SENDER_EMAIL    = "EMAIL_USER"
SENDER_PASSWORD = "EMAIL_PASS"

# LOADING MODEL
with open('flood_model.pkl', 'rb') as f:
    model = pickle.load(f)

# LOCATING DATA
province_districts = {
    'Sindh': ['Dadu', 'Jacobabad', 'Kambar', 'Khairpur', 'Mirpur Khas',
              'Jamshoro', 'Sanghar', 'Badin', 'Sukkur', 'Larkana'],
    'Balochistan': ['Quetta', 'Kharan', 'Washuk', 'Jaffarabad', 'Jhal Magsi',
                    'Sohbatpur', 'Naseerabad', 'Lasbela', 'Kech', 'Panjgur'],
    'KPK': ['Swat', 'Nowshera', 'Charsadda', 'Peshawar', 'DI Khan',
            'Lower Dir', 'Upper Dir', 'Chitral', 'Kohistan', 'Buner'],
    'Punjab': ['Taunsa', 'Dera Ghazi Khan', 'Rajanpur', 'Muzaffargarh',
               'Layyah', 'Bhakkar', 'Mianwali', 'Bahawalpur', 'RY Khan', 'Multan'],
    'Gilgit_Baltistan': ['Ghizer', 'Nagar', 'Diamer', 'Ghanche', 'Astore',
                         'Gilgit', 'Hunza', 'Skardu', 'Shigar', 'Kharmang']
}

district_cities = {
    'Dadu':             ['Johi', 'Mehar', 'Khairpur Nathan Shah', 'Warah', 'Dadu City', 'Sehwan'],
    'Jacobabad':        ['Jacobabad City', 'Garhi Khairo', 'Thull', 'Mirpur Mathelo'],
    'Kambar':           ['Kambar City', 'Shahdadkot', 'Warah', 'Mirokhan'],
    'Khairpur':         ['Khairpur City', 'Kot Diji', 'Gambat', 'Kingri', 'Thari Mirwah'],
    'Mirpur Khas':      ['Mirpur Khas City', 'Digri', 'Jhuddo', 'Sindhri'],
    'Jamshoro':         ['Jamshoro City', 'Kotri', 'Sehwan', 'Manjhand'],
    'Sanghar':          ['Sanghar City', 'Shahdadpur', 'Tando Adam', 'Sinjhoro'],
    'Badin':            ['Badin City', 'Matli', 'Talhar', 'Golarchi', 'Tando Bago'],
    'Sukkur':           ['Sukkur City', 'Rohri', 'Pano Aqil', 'Saleh Pat'],
    'Larkana':          ['Larkana City', 'Dokri', 'Ratodero', 'Bakrani'],
    'Quetta':           ['Quetta City', 'Satellite Town', 'Sariab', 'Kuchlak'],
    'Kharan':           ['Kharan City', 'Nushki', 'Yakmach'],
    'Washuk':           ['Washuk City', 'Khuzdar', 'Turbat'],
    'Jaffarabad':       ['Dera Allah Yar', 'Gandakha', 'Sohbatpur'],
    'Jhal Magsi':       ['Jhal Magsi City', 'Gandava', 'Khattan'],
    'Sohbatpur':        ['Sohbatpur City', 'Dera Allah Yar', 'Jhatpat'],
    'Naseerabad':       ['Tamboo', 'Dera Murad Jamali', 'Loti'],
    'Lasbela':          ['Uthal', 'Hub', 'Bela', 'Winder'],
    'Kech':             ['Turbat', 'Mand', 'Buleda'],
    'Panjgur':          ['Panjgur City', 'Gichk', 'Parpach'],
    'Swat':             ['Mingora', 'Matta', 'Khwazakhela', 'Bahrain', 'Madyan'],
    'Nowshera':         ['Nowshera City', 'Pabbi', 'Jehangira'],
    'Charsadda':        ['Charsadda City', 'Tangi', 'Shabqadar'],
    'Peshawar':         ['Peshawar City', 'Hayatabad', 'Warsak', 'Mattni'],
    'DI Khan':          ['DI Khan City', 'Paharpur', 'Kulachi', 'Tank'],
    'Lower Dir':        ['Timergara', 'Munda', 'Balambat'],
    'Upper Dir':        ['Dir City', 'Wari', 'Sheringal'],
    'Chitral':          ['Chitral City', 'Mastuj', 'Booni'],
    'Kohistan':         ['Dassu', 'Pattan', 'Komila'],
    'Buner':            ['Daggar', 'Totalai', 'Chamla'],
    'Taunsa':           ['Taunsa City', 'Choti Zarin', 'Kot Sultan'],
    'Dera Ghazi Khan':  ['DG Khan City', 'Taunsa', 'Kot Chutta', 'Vehova'],
    'Rajanpur':         ['Rajanpur City', 'Jampur', 'Rojhan'],
    'Muzaffargarh':     ['Muzaffargarh City', 'Kot Addu', 'Ali Pur', 'Jatoi'],
    'Layyah':           ['Layyah City', 'Chowk Azam', 'Karor'],
    'Bhakkar':          ['Bhakkar City', 'Darya Khan', 'Mankera'],
    'Mianwali':         ['Mianwali City', 'Piplan', 'Isa Khel'],
    'Bahawalpur':       ['Bahawalpur City', 'Ahmadpur East', 'Khairpur Tamewali'],
    'RY Khan':          ['Rahim Yar Khan City', 'Sadiqabad', 'Liaquatpur'],
    'Multan':           ['Multan City', 'Shujabad', 'Jalalpur Pirwala'],
    'Ghizer':           ['Gahkuch', 'Phander', 'Teru'],
    'Nagar':            ['Nagar City', 'Hispar', 'Hopar'],
    'Diamer':           ['Chilas', 'Darel', 'Tangir'],
    'Ghanche':          ['Khaplu', 'Saltoro', 'Shyok'],
    'Astore':           ['Astore City', 'Rattu', 'Minimarg'],
    'Gilgit':           ['Gilgit City', 'Jutial', 'Konodas'],
    'Hunza':            ['Karimabad', 'Aliabad', 'Ganish'],
    'Skardu':           ['Skardu City', 'Shigar', 'Rondu'],
    'Shigar':           ['Shigar City', 'Askole', 'Basha'],
    'Kharmang':         ['Kharmang City', 'Gol', 'Tolti'],
}


# RELIEF CENTERS DATABSE
relief_centers_db = {
    'Dadu':             [{'name':'PDMA Dadu Relief Camp','address':'Near DC Office, Dadu','email':'pdma.dadu@sindh.gov.pk','phone':'025-4610001'},
                         {'name':'Pakistan Red Crescent — Dadu','address':'Main Bazaar Road, Dadu','email':'prc.dadu@redcrescent.pk','phone':'115'},
                         {'name':'Edhi Foundation — Dadu','address':'Hospital Road, Dadu','email':'dadu@edhi.org','phone':'115'}],
    'Jacobabad':        [{'name':'PDMA Jacobabad Relief Camp','address':'Near DC Office, Jacobabad','email':'pdma.jacobabad@sindh.gov.pk','phone':'0722-651001'},
                         {'name':'Pakistan Red Crescent — Jacobabad','address':'Bypass Road, Jacobabad','email':'prc.jacobabad@redcrescent.pk','phone':'115'}],
    'Kambar':           [{'name':'PDMA Kambar Relief Camp','address':'Main Road, Kambar','email':'pdma.kambar@sindh.gov.pk','phone':'0748-520001'},
                         {'name':'Edhi Foundation — Kambar','address':'Shahdadkot Road, Kambar','email':'kambar@edhi.org','phone':'115'}],
    'Khairpur':         [{'name':'PDMA Khairpur Relief Camp','address':'Near DC Office, Khairpur','email':'pdma.khairpur@sindh.gov.pk','phone':'0243-712001'},
                         {'name':'Pakistan Red Crescent — Khairpur','address':'Station Road, Khairpur','email':'prc.khairpur@redcrescent.pk','phone':'115'}],
    'Mirpur Khas':      [{'name':'PDMA Mirpur Khas Relief Camp','address':'Near DC Office, Mirpur Khas','email':'pdma.mpk@sindh.gov.pk','phone':'0233-871001'},
                         {'name':'Edhi Foundation — Mirpur Khas','address':'Hyderabad Road, Mirpur Khas','email':'mpk@edhi.org','phone':'115'}],
    'Jamshoro':         [{'name':'PDMA Jamshoro Relief Camp','address':'Near DC Office, Jamshoro','email':'pdma.jamshoro@sindh.gov.pk','phone':'022-2772001'},
                         {'name':'Pakistan Red Crescent — Jamshoro','address':'University Road, Jamshoro','email':'prc.jamshoro@redcrescent.pk','phone':'115'}],
    'Sanghar':          [{'name':'PDMA Sanghar Relief Camp','address':'Near DC Office, Sanghar','email':'pdma.sanghar@sindh.gov.pk','phone':'0235-541001'},
                         {'name':'Edhi Foundation — Sanghar','address':'Main Road, Sanghar','email':'sanghar@edhi.org','phone':'115'}],
    'Badin':            [{'name':'PDMA Badin Relief Camp','address':'Near DC Office, Badin','email':'pdma.badin@sindh.gov.pk','phone':'0297-862001'},
                         {'name':'Pakistan Red Crescent — Badin','address':'Station Road, Badin','email':'prc.badin@redcrescent.pk','phone':'115'}],
    'Sukkur':           [{'name':'PDMA Sukkur Relief Camp','address':'Near DC Office, Sukkur','email':'pdma.sukkur@sindh.gov.pk','phone':'071-5630001'},
                         {'name':'Edhi Foundation — Sukkur','address':'Barrage Road, Sukkur','email':'sukkur@edhi.org','phone':'115'},
                         {'name':'Pakistan Red Crescent — Sukkur','address':'Military Road, Sukkur','email':'prc.sukkur@redcrescent.pk','phone':'115'}],
    'Larkana':          [{'name':'PDMA Larkana Relief Camp','address':'Near DC Office, Larkana','email':'pdma.larkana@sindh.gov.pk','phone':'074-4050001'},
                         {'name':'Pakistan Red Crescent — Larkana','address':'Station Road, Larkana','email':'prc.larkana@redcrescent.pk','phone':'115'}],
    'Quetta':           [{'name':'PDMA Balochistan HQ','address':'Civil Secretariat, Quetta','email':'pdma@balochistan.gov.pk','phone':'081-9201601'},
                         {'name':'Pakistan Red Crescent — Quetta','address':'Jinnah Road, Quetta','email':'prc.quetta@redcrescent.pk','phone':'115'},
                         {'name':'Edhi Foundation — Quetta','address':'Shahrah-e-Iqbal, Quetta','email':'quetta@edhi.org','phone':'115'}],
    'Jaffarabad':       [{'name':'PDMA Jaffarabad Relief Camp','address':'Near DC Office, Dera Allah Yar','email':'pdma.jaffarabad@balochistan.gov.pk','phone':'0834-270001'},
                         {'name':'Edhi Foundation — Jaffarabad','address':'Main Road, Dera Allah Yar','email':'jaffarabad@edhi.org','phone':'115'}],
    'Naseerabad':       [{'name':'PDMA Naseerabad Relief Camp','address':'Near DC Office, DMJ','email':'pdma.naseerabad@balochistan.gov.pk','phone':'0833-710001'},
                         {'name':'Pakistan Red Crescent — Naseerabad','address':'Bypass Road, DMJ','email':'prc.naseerabad@redcrescent.pk','phone':'115'}],
    'Lasbela':          [{'name':'PDMA Lasbela Relief Camp','address':'Near DC Office, Uthal','email':'pdma.lasbela@balochistan.gov.pk','phone':'0853-610001'},
                         {'name':'Edhi Foundation — Hub','address':'Industrial Area, Hub','email':'hub@edhi.org','phone':'115'}],
    'Swat':             [{'name':'PDMA Swat Relief Camp','address':'Near DC Office, Mingora','email':'pdma.swat@kp.gov.pk','phone':'0946-720001'},
                         {'name':'Pakistan Red Crescent — Swat','address':'Saidu Road, Mingora','email':'prc.swat@redcrescent.pk','phone':'115'},
                         {'name':'Edhi Foundation — Swat','address':'GT Road, Mingora','email':'swat@edhi.org','phone':'115'}],
    'Nowshera':         [{'name':'PDMA Nowshera Relief Camp','address':'Near DC Office, Nowshera','email':'pdma.nowshera@kp.gov.pk','phone':'0923-610001'},
                         {'name':'Pakistan Red Crescent — Nowshera','address':'GT Road, Nowshera','email':'prc.nowshera@redcrescent.pk','phone':'115'}],
    'Peshawar':         [{'name':'PDMA KPK HQ Peshawar','address':'Civil Secretariat, Peshawar','email':'pdma@kp.gov.pk','phone':'091-9210601'},
                         {'name':'Edhi Foundation — Peshawar','address':'University Road, Peshawar','email':'peshawar@edhi.org','phone':'115'},
                         {'name':'Pakistan Red Crescent — Peshawar','address':'Khyber Road, Peshawar','email':'prc.peshawar@redcrescent.pk','phone':'115'}],
    'DI Khan':          [{'name':'PDMA DI Khan Relief Camp','address':'Near DC Office, DI Khan','email':'pdma.dikan@kp.gov.pk','phone':'0966-710001'},
                         {'name':'Pakistan Red Crescent — DI Khan','address':'Circular Road, DI Khan','email':'prc.dikan@redcrescent.pk','phone':'115'}],
    'Dera Ghazi Khan':  [{'name':'PDMA DG Khan Relief Camp','address':'Near DC Office, DG Khan','email':'pdma.dgkhan@punjab.gov.pk','phone':'064-9260301'},
                         {'name':'Pakistan Red Crescent — DG Khan','address':'Railway Road, DG Khan','email':'prc.dgkhan@redcrescent.pk','phone':'115'},
                         {'name':'Edhi Foundation — DG Khan','address':'Multan Road, DG Khan','email':'dgkhan@edhi.org','phone':'115'}],
    'Rajanpur':         [{'name':'PDMA Rajanpur Relief Camp','address':'Near DC Office, Rajanpur','email':'pdma.rajanpur@punjab.gov.pk','phone':'0604-540001'},
                         {'name':'Pakistan Red Crescent — Rajanpur','address':'Main Bazaar, Rajanpur','email':'prc.rajanpur@redcrescent.pk','phone':'115'}],
    'Muzaffargarh':     [{'name':'PDMA Muzaffargarh Relief Camp','address':'Near DC Office, Muzaffargarh','email':'pdma.mzg@punjab.gov.pk','phone':'066-9200301'},
                         {'name':'Edhi Foundation — Muzaffargarh','address':'Multan Road, Muzaffargarh','email':'mzg@edhi.org','phone':'115'}],
    'Gilgit':           [{'name':'PDMA GB HQ Gilgit','address':'Civil Secretariat, Gilgit','email':'pdma@gilgitbaltistan.gov.pk','phone':'05811-920001'},
                         {'name':'Pakistan Red Crescent — Gilgit','address':'Aga Khan Road, Gilgit','email':'prc.gilgit@redcrescent.pk','phone':'115'}],
    'Skardu':           [{'name':'PDMA Skardu Relief Camp','address':'Near DC Office, Skardu','email':'pdma.skardu@gilgitbaltistan.gov.pk','phone':'05841-920001'},
                         {'name':'Edhi Foundation — Skardu','address':'Main Bazaar, Skardu','email':'skardu@edhi.org','phone':'115'}],
}

def get_relief_centers(district):
    if district in relief_centers_db:
        return relief_centers_db[district]
    return [
        {'name': f'PDMA {district} Relief Camp',
         'address': f'Near Deputy Commissioner Office, {district}',
         'email': f'pdma.{district.lower().replace(" ","").replace("_","")}@gov.pk',
         'phone': '1199'},
        {'name': f'Pakistan Red Crescent — {district}',
         'address': f'Main Road, {district}',
         'email': 'info@redcrescent.pk',
         'phone': '115'},
        {'name': f'Edhi Foundation — {district}',
         'address': f'Hospital Road, {district}',
         'email': 'info@edhi.org',
         'phone': '115'},
    ]


# MODEL ENCODING
province_codes  = {p: i for i, p in enumerate(sorted(province_districts.keys()))}
all_districts   = sorted([d for dists in province_districts.values() for d in dists])
TRAINED_COLUMNS = ['province', 'district', 'monthly_income_pkr', 'family_size',
                   'house_condition', 'distance_from_relief_center_km',
                   'previous_flood_damage', 'access_to_clean_water',
                   'livestock_lost', 'crops_damaged', 'children_under_age_5',
                   'disabled_family_members', 'flood_risk_level']


# HELPER FUNCTIONS
def run_prediction(province, district, monthly_income, family_size,
                   house_condition, distance, previous_damage, clean_water,
                   livestock_lost, crops_damaged, children_under_5,
                   disabled_members, flood_risk):
    p_code = province_codes[province]
    d_code = all_districts.index(district)
    df = pd.DataFrame([{
        'province':                       p_code,
        'district':                       d_code,
        'monthly_income_pkr':             monthly_income,
        'family_size':                    family_size,
        'house_condition':                house_condition,
        'distance_from_relief_center_km': distance,
        'previous_flood_damage':          1 if previous_damage == "Yes" else 0,
        'access_to_clean_water':          1 if clean_water      == "Yes" else 0,
        'livestock_lost':                 1 if livestock_lost    == "Yes" else 0,
        'crops_damaged':                  1 if crops_damaged     == "Yes" else 0,
        'children_under_age_5':           children_under_5,
        'disabled_family_members':        1 if disabled_members  == "Yes" else 0,
        'flood_risk_level':               flood_risk,
    }])[TRAINED_COLUMNS]
    pred  = model.predict(df)[0]
    prob = model.predict_proba(df)[0]
    return int(pred), prob


def log_to_csv(data: dict):
    path        = 'submissions_log.csv'
    file_exists = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(data.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def send_relief_email(center: dict, household: dict,
                      personal: dict, confidence: float) -> tuple:
    try:
        msg            = MIMEMultipart()
        msg['From']    = SENDER_EMAIL
        msg['To']      = center['email']
        msg['Subject'] = (f"URGENT FLOOD AID REQUEST — {personal['full_name']} "
                          f"| {household['city']}, {household['district']} "
                          f"| {confidence:.1f}% Confidence")
        body = f"""
PAKISTAN FLOOD AID PREDICTOR — URGENT AID REQUEST
==================================================
Generated  : {datetime.now().strftime('%d %b %Y  %H:%M')}
Confidence : {confidence:.1f}%

APPLICANT DETAILS
-----------------
Full Name  : {personal['full_name']}
CNIC       : {personal.get('cnic','Not provided')}
Contact    : {personal.get('contact','Not provided')}
Address    : {personal['address']}

LOCATION
--------
Province   : {household['province']}
District   : {household['district']}
City/Town  : {household['city']}

HOUSEHOLD PROFILE
-----------------
Monthly Income   : PKR {household['monthly_income']:,}
Family Size      : {household['family_size']} members
Flood Risk       : {household['flood_risk_label']} ({household['flood_risk_value']}/10)
House Condition  : {household['house_condition_label']}
Distance to RC   : {household['distance']} km

VULNERABILITY INDICATORS
------------------------
Previous Flood Damage  : {household['previous_damage']}
Access to Clean Water  : {household['clean_water']}
Livestock Lost         : {household['livestock_lost']}
Crops Damaged          : {household['crops_damaged']}
Children Under 5       : {household['children_under_5']}
Elderly Members (60+)  : {household['elderly_members']}
Disabled Members       : {household['disabled_members']}
Medical Emergency      : {household['medical_emergency']}

NEAREST RELIEF CENTER
---------------------
{center['name']}
{center['address']}
Phone : {center['phone']}
Email : {center['email']}

This household has been assessed as REQUIRING URGENT AID
with {confidence:.1f}% model confidence. Please prioritise
this case in your relief distribution operations.

--
Pakistan Flood Aid Predictor
ML Model: Random Forest | Accuracy: 87.36%
Data Source: IOM DTM Pakistan 2022 | Households: 14,320
        """
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)


# SESSION STATE
for key, default in [
    ('prediction', None), ('confidence', None),
    ('household_snapshot', None), ('show_send_form', False),
    ('email_sent', False), ('selected_center', None),
    ('personal_data', None), ('email_success', False), ('email_msg', ''),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# PAGE CONFIG & CSS
st.set_page_config(
    page_title="Pakistan Flood Aid Predictor",
    page_icon="🌊",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Source+Sans+3:wght@300;400;500;600&display=swap');

:root {
    --bg:     #05111f;
    --card:   #0d2035;
    --teal:   #00d4b8;
    --teal2:  #009e8a;
    --amber:  #f5a623;
    --red:    #f04040;
    --green:  #10c97a;
    --muted:  #6b8aaa;
    --text:   #dce8f5;
    --border: rgba(0,212,184,.14);
    --bord2:  rgba(0,212,184,.28);
}

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}
.stApp {
    background: linear-gradient(160deg, #05111f 0%, #081722 60%, #05111f 100%) !important;
}

/* Header */
.app-header {
    background: linear-gradient(90deg, rgba(0,212,184,.07), rgba(245,166,35,.04));
    border: 1px solid var(--bord2);
    border-radius: 18px;
    padding: 34px 44px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--teal), var(--amber), var(--teal));
}
.app-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: 1px;
    line-height: 1;
    margin: 0;
}
.app-title span { color: var(--teal); }
.app-sub {
    color: var(--muted);
    font-size: .95rem;
    margin-top: 6px;
    font-weight: 300;
    letter-spacing: .4px;
}

/* Stats */
.stats-row { display: flex; gap: 16px; margin-bottom: 26px; flex-wrap: wrap; }
.stat-pill {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 22px;
    flex: 1;
    min-width: 110px;
    text-align: center;
}
.stat-num {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--teal);
    line-height: 1;
}
.stat-lbl {
    font-size: .7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 3px;
}

/* Section label */
.sec-lbl {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--teal);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    border-left: 3px solid var(--teal);
    padding-left: 10px;
    margin: 18px 0 12px;
}

/* Relief center cards */
.rc-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 6px 0;
}
.rc-card.selected {
    border-color: var(--teal);
    background: rgba(0,212,184,.05);
}
.rc-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--teal);
}
.rc-meta { color: var(--muted); font-size: .8rem; margin-top: 4px; line-height: 1.7; }

/* Predict button */
.stButton > button {
    background: linear-gradient(90deg, var(--teal2), var(--teal)) !important;
    color: #000 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px !important;
    width: 100% !important;
    text-transform: uppercase !important;
    transition: all .25s !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 22px rgba(0,212,184,.38) !important;
    transform: translateY(-1px) !important;
}

/* Result cards */
.result-aid {
    background: linear-gradient(135deg, rgba(240,64,64,.14), rgba(240,64,64,.04));
    border: 1px solid rgba(240,64,64,.38);
    border-left: 4px solid var(--red);
    border-radius: 14px;
    padding: 24px 28px;
    margin-top: 14px;
}
.result-ok {
    background: linear-gradient(135deg, rgba(16,201,122,.12), rgba(16,201,122,.03));
    border: 1px solid rgba(16,201,122,.35);
    border-left: 4px solid var(--green);
    border-radius: 14px;
    padding: 24px 28px;
    margin-top: 14px;
}
.res-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: .5px;
    margin: 0 0 6px;
}
.res-desc { color: var(--muted); font-size: .88rem; }
.conf-num {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    margin-top: 10px;
}
.conf-bar {
    height: 5px;
    background: rgba(255,255,255,.1);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 6px;
}
.conf-fill-r { height: 100%; background: linear-gradient(90deg, var(--red), #ff7070); border-radius: 3px; }
.conf-fill-g { height: 100%; background: linear-gradient(90deg, var(--green), #5df5af); border-radius: 3px; }

/* Send box */
.send-box {
    background: linear-gradient(135deg, rgba(245,166,35,.09), rgba(245,166,35,.02));
    border: 1px solid rgba(245,166,35,.28);
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 14px;
}
.send-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--amber);
    margin-bottom: 4px;
}

/* Confirm box */
.confirm-box {
    background: linear-gradient(135deg, rgba(16,201,122,.1), rgba(0,212,184,.04));
    border: 1px solid rgba(16,201,122,.3);
    border-radius: 12px;
    padding: 22px 26px;
    margin-top: 14px;
}
.confirm-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--green);
    margin-bottom: 10px;
}
.crow { display: flex; gap: 8px; margin: 4px 0; font-size: .87rem; color: var(--muted); }
.crow span { color: var(--text); font-weight: 500; }

/* Inputs */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--card) !important;
    border: 1px solid var(--bord2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
label, .stSlider label, .stRadio > label {
    color: var(--muted) !important;
    font-size: .82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: .5px !important;
}

/* Footer */
.app-footer {
    text-align: center;
    color: var(--muted);
    font-size: .73rem;
    padding: 18px;
    border-top: 1px solid var(--border);
    margin-top: 36px;
    letter-spacing: .4px;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="app-header">
  <div class="app-title">🌊 PAKISTAN <span>FLOOD AID</span> PREDICTOR</div>
  <div class="app-sub">AI-powered humanitarian relief distribution system — 2022 Pakistan Floods Response</div>
</div>
""", unsafe_allow_html=True)


# STATS
st.markdown("""
<div class="stats-row">
  <div class="stat-pill"><div class="stat-num">33M+</div><div class="stat-lbl">People Affected</div></div>
  <div class="stat-pill"><div class="stat-num">1.7M</div><div class="stat-lbl">Houses Damaged</div></div>
  <div class="stat-pill"><div class="stat-num">116</div><div class="stat-lbl">Districts Affected</div></div>
  <div class="stat-pill"><div class="stat-num">14,320</div><div class="stat-lbl">Households in Dataset</div></div>
  <div class="stat-pill"><div class="stat-num">87.36%</div><div class="stat-lbl">Model Accuracy</div></div>
</div>
""", unsafe_allow_html=True)


# LOCATION
st.markdown('<div class="sec-lbl">📍 Location</div>', unsafe_allow_html=True)

lc1, lc2, lc3 = st.columns(3)
with lc1:
    province = st.selectbox("Province", list(province_districts.keys()))
with lc2:
    district = st.selectbox("District", province_districts[province])
with lc3:
    cities = district_cities.get(district, [district + ' City'])
    city   = st.selectbox("City / Town", cities)


# RELIEF CENTERS
centers = get_relief_centers(district)
st.markdown('<div class="sec-lbl">🏥 Nearby Flood Relief Centers</div>', unsafe_allow_html=True)

selected_center_name = st.radio(
    "Select nearest center:",
    [c['name'] for c in centers],
    label_visibility="collapsed"
)
selected_center = next(c for c in centers if c['name'] == selected_center_name)
st.session_state.selected_center = selected_center

st.markdown(f"""
<div class="rc-card selected">
  <div class="rc-name">📍 {selected_center['name']}</div>
  <div class="rc-meta">
    🗺 {selected_center['address']}<br>
    📧 {selected_center['email']}<br>
    📞 {selected_center['phone']}
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# HOUSEHOLD DETAILS
st.markdown('<div class="sec-lbl">🏠 Household Details</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Financial & Family**")
    monthly_income       = st.number_input("Monthly Income (PKR)", min_value=3000, max_value=80000, value=15000, step=500)
    family_size          = st.slider("Family Size", min_value=2, max_value=15, value=5)
    children_under_age_5 = st.slider("Children Under Age 5", min_value=0, max_value=8, value=1)
    elderly_members      = st.slider("Elderly Members (60+)", min_value=0, max_value=6, value=0)

with col2:
    st.markdown("**Property & Risk**")

    st.markdown("**House Condition**")
    house_condition_label = st.radio(
        "hc", ["Poor", "Fair", "Good", "Excellent"],
        horizontal=True, label_visibility="collapsed"
    )
    house_condition = {"Poor": 1, "Fair": 2, "Good": 3, "Excellent": 4}[house_condition_label]

    st.markdown("**Flood Risk Level**")
    flood_risk_label = st.radio(
        "fr", ["Low", "Medium", "High"],
        horizontal=True, label_visibility="collapsed"
    )
    flood_risk = {"Low": 3, "Medium": 6, "High": 9}[flood_risk_label]

    distance = st.number_input("Distance from Relief Center (km)",
                               min_value=1, max_value=300, value=20, step=1)

with col3:
    st.markdown("**Situation Assessment**")
    previous_damage   = st.radio("Previous Flood Damage?",        ["Yes", "No"], horizontal=True)
    clean_water       = st.radio("Access to Clean Water?",         ["Yes", "No"], horizontal=True)
    livestock_lost    = st.radio("Livestock Lost?",                ["Yes", "No"], horizontal=True)
    crops_damaged     = st.radio("Crops Damaged?",                 ["Yes", "No"], horizontal=True)
    disabled_members  = st.radio("Disabled Family Members?",       ["Yes", "No"], horizontal=True)
    medical_emergency = st.radio("Medical Emergency in Household?",["Yes", "No"], horizontal=True)

st.markdown("---")


# PREDICT BUTTON
if st.button("⚡  ASSESS AID REQUIREMENT", use_container_width=True):

    pred, proba = run_prediction(
        province, district, monthly_income, family_size,
        house_condition, distance, previous_damage, clean_water,
        livestock_lost, crops_damaged, children_under_age_5,
        disabled_members, flood_risk
    )

    st.session_state.prediction         = pred
    st.session_state.confidence         = proba[1] * 100 if pred == 1 else proba[0] * 100
    st.session_state.show_send_form     = False
    st.session_state.email_sent         = False
    st.session_state.household_snapshot = {
        'province':              province,
        'district':              district,
        'city':                  city,
        'monthly_income':        monthly_income,
        'family_size':           family_size,
        'flood_risk_label':      flood_risk_label,
        'flood_risk_value':      flood_risk,
        'house_condition_label': house_condition_label,
        'distance':              distance,
        'previous_damage':       previous_damage,
        'clean_water':           clean_water,
        'livestock_lost':        livestock_lost,
        'crops_damaged':         crops_damaged,
        'children_under_5':      children_under_age_5,
        'elderly_members':       elderly_members,
        'disabled_members':      disabled_members,
        'medical_emergency':     medical_emergency,
    }


# PREDICTION RESULT
if st.session_state.prediction is not None:
    pred = st.session_state.prediction
    conf = st.session_state.confidence
    hh   = st.session_state.household_snapshot

    st.markdown("---")

    if pred == 1:
        st.markdown(f"""
        <div class="result-aid">
          <div class="res-title" style="color:var(--red)">🚨 AID REQUIRED</div>
          <div class="res-desc">This household requires urgent flood relief assistance based on the assessed conditions.</div>
          <div class="conf-num" style="color:var(--red)">{conf:.1f}% Confidence</div>
          <div class="conf-bar"><div class="conf-fill-r" style="width:{conf}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

        if conf >= 80:
            st.error("⚠️ **CRITICAL PRIORITY** — Immediate relief deployment recommended.")
        elif conf >= 60:
            st.warning("🟡 **HIGH PRIORITY** — Relief needed within 24 hours.")
        else:
            st.info("🔵 **MODERATE PRIORITY** — Include in next relief distribution round.")

        st.markdown("")

        if not st.session_state.show_send_form and not st.session_state.email_sent:
            if st.button("📤  SEND DATA TO NEAREST RELIEF CENTER", use_container_width=True):
                st.session_state.show_send_form = True
                st.rerun()

    else:
        st.markdown(f"""
        <div class="result-ok">
          <div class="res-title" style="color:var(--green)">✅ AID NOT REQUIRED</div>
          <div class="res-desc">This household does not currently qualify for priority flood relief assistance.</div>
          <div class="conf-num" style="color:var(--green)">{conf:.1f}% Confidence</div>
          <div class="conf-bar"><div class="conf-fill-g" style="width:{conf}%"></div></div>
        </div>
        """, unsafe_allow_html=True)


# PERSONAL INFO FORM
if st.session_state.show_send_form and not st.session_state.email_sent:

    center = st.session_state.selected_center
    conf   = st.session_state.confidence

    st.markdown(f"""
    <div class="send-box">
      <div class="send-title">📤 Send Aid Request to {center['name']}</div>
      <div style="color:var(--muted);font-size:.85rem">
        Fill in the applicant's personal details. All information will be
        emailed to the relief center automatically.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    pf1, pf2 = st.columns(2)
    with pf1:
        full_name = st.text_input("Full Name *", placeholder="e.g. Muhammad Ali Shah")
        cnic      = st.text_input("CNIC Number (optional)", placeholder="e.g. 42301-1234567-1")
    with pf2:
        contact   = st.text_input("Contact Number (if any)", placeholder="e.g. 0300-1234567")
        address   = st.text_area("Current Detailed Address *",
                                 placeholder="House No., Street, Mohalla, City, District",
                                 height=100)

    st.markdown("")
    sc, cc = st.columns([3, 1])
    with sc:
        submit_clicked = st.button("✉️  SUBMIT & SEND TO RELIEF CENTER", use_container_width=True)
    with cc:
        if st.button("Cancel", use_container_width=True):
            st.session_state.show_send_form = False
            st.rerun()

    if submit_clicked:
        if not full_name.strip():
            st.error("Please enter the applicant's full name.")
        elif not address.strip():
            st.error("Please enter the current address.")
        else:
            personal = {
                'full_name': full_name.strip(),
                'cnic':      cnic.strip()    if cnic.strip()    else 'Not provided',
                'contact':   contact.strip() if contact.strip() else 'Not provided',
                'address':   address.strip(),
            }
            hh = st.session_state.household_snapshot

            with st.spinner("Sending to relief center..."):
                success, msg = send_relief_email(center, hh, personal, conf)

            log_to_csv({
                'timestamp':      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'full_name':      personal['full_name'],
                'cnic':           personal['cnic'],
                'contact':        personal['contact'],
                'address':        personal['address'],
                'province':       hh['province'],
                'district':       hh['district'],
                'city':           hh['city'],
                'income_pkr':     hh['monthly_income'],
                'family_size':    hh['family_size'],
                'flood_risk':     hh['flood_risk_label'],
                'house':          hh['house_condition_label'],
                'prediction':     'AID REQUIRED',
                'confidence_pct': f"{conf:.1f}",
                'relief_center':  center['name'],
                'email_sent':     'Yes' if success else 'No',
            })

            st.session_state.show_send_form = False
            st.session_state.email_sent     = True
            st.session_state.personal_data  = personal
            st.session_state.email_success  = success
            st.session_state.email_msg      = msg
            st.rerun()


# CONFIRMATION SCREEN

if st.session_state.email_sent:

    hh      = st.session_state.household_snapshot
    center  = st.session_state.selected_center
    conf    = st.session_state.confidence
    person  = st.session_state.personal_data  or {}
    success = st.session_state.email_success
    emsg    = st.session_state.email_msg

    if success:
        st.success(f"✅ Data successfully sent to **{center['name']}**!")
        st.balloons()
    else:
        st.warning(f"⚠️ Email could not be delivered automatically ({emsg}). "
                   f"Please call the relief center directly: **{center['phone']}**")

    st.markdown(f"""
    <div class="confirm-box">
      <div class="confirm-title">📋 Submission Summary</div>

      <div class="crow">🎯 Prediction: <span style="color:var(--red);font-weight:700">AID REQUIRED — {conf:.1f}% Confidence</span></div>
      <div class="crow">🏥 Relief Center: <span>{center['name']}</span></div>
      <div class="crow">📧 Sent To: <span>{center['email']}</span></div>
      <div class="crow">📞 Phone: <span>{center['phone']}</span></div>
      <br>
      <div class="crow">👤 Applicant: <span>{person.get('full_name','—')}</span></div>
      <div class="crow">🪪 CNIC: <span>{person.get('cnic','Not provided')}</span></div>
      <div class="crow">📱 Contact: <span>{person.get('contact','Not provided')}</span></div>
      <div class="crow">🗺 Address: <span>{person.get('address','—')}</span></div>
      <br>
      <div class="crow">📍 Location: <span>{hh['city']}, {hh['district']}, {hh['province']}</span></div>
      <div class="crow">💰 Income: <span>PKR {hh['monthly_income']:,}/month</span></div>
      <div class="crow">👨‍👩‍👧 Family: <span>{hh['family_size']} members</span></div>
      <div class="crow">🌊 Flood Risk: <span>{hh['flood_risk_label']}</span></div>
      <div class="crow">🕐 Submitted: <span>{datetime.now().strftime('%d %b %Y — %H:%M')}</span></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Submit Another Assessment", use_container_width=True):
        for k in ['prediction', 'confidence', 'household_snapshot',
                  'show_send_form', 'email_sent', 'personal_data',
                  'email_success', 'email_msg']:
            st.session_state[k] = None if k in ['prediction', 'confidence',
                                                  'household_snapshot', 'personal_data'] else False
        st.rerun()


# VISUALIZATIONS
st.markdown("---")
show_visualizations()


# FOOTER
st.markdown("""
<div class="app-footer">
  Data Source: IOM DTM Pakistan Flood Response 2022 — OCHA HDX &nbsp;|&nbsp;
  ML Model: Random Forest Classifier &nbsp;|&nbsp;
  Accuracy: 87.36% &nbsp;|&nbsp;
  Dataset: 14,320 Households — 5 Provinces
</div>
""", unsafe_allow_html=True)