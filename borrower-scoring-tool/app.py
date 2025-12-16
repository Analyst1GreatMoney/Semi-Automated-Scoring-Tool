# =====================================================
# Imports
# =====================================================
import streamlit as st
import pandas as pd
from pathlib import Path


# =====================================================
# Session State
# =====================================================
if "run_collateral_assessment" not in st.session_state:
    st.session_state["run_collateral_assessment"] = False


# =====================================================
# Resolve Repo Root
# pages/1_Collateral_Review.py
# =====================================================
BASE_DIR = Path(__file__).resolve().parents[2]


# =====================================================
# Utility: Suburb Normalisation
# =====================================================
def normalise_suburb_name(name: str) -> str:
    if pd.isna(name):
        return ""
    return (
        name.upper()
        .replace("(NSW)", "")
        .replace("(VIC)", "")
        .replace("(QLD)", "")
        .replace("(WA)", "")
        .replace("(SA)", "")
        .replace("(TAS)", "")
        .replace("(ACT)", "")
        .replace("(NT)", "")
        .strip()
    )


# =====================================================
# Scoring Definitions (Policy Layer)
# =====================================================
def load_irsd_scoring_table():
    return pd.DataFrame({
        "IRSD_Decile": range(1, 11),
        "Score": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    })


def load_irsad_scoring_table():
    return pd.DataFrame({
        "IRSAD_Decile": range(1, 11),
        "Score": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    })


def crime_score_from_percentile(percentile: float) -> int:
    if percentile >= 90:
        return 100
    elif percentile >= 75:
        return 80
    elif percentile >= 50:
        return 60
    elif percentile >= 25:
        return 40
    else:
        return 20


def calculate_location_risk_score(crime_score, irsd_score, irsad_score):
    return round(
        0.4 * crime_score +
        0.3 * irsd_score +
        0.3 * irsad_score,
        1
    )


def classify_location_risk(score):
    if score >= 75:
        return "Low Risk", "🟢"
    elif score >= 50:
        return "Moderate Risk", "🟡"
    else:
        return "Elevated Risk", "🔴"


# =====================================================
# Data Loading (Data Layer)
# =====================================================
@st.cache_data
def load_crime_data():
    path = BASE_DIR / "doc" / "Collateral" / "data" / \
        "suburb_crime_risk_12m_2024_07_to_2025_06.csv"
    df = pd.read_csv(path)
    df["SUBURB_KEY"] = df["Suburb"].apply(normalise_suburb_name)
    df["crime_percentile"] = (
        df["crime_12m"].rank(pct=True, ascending=True) * 100
    )
    return df


@st.cache_data
def load_seifa_data():
    path = BASE_DIR / "doc" / "Collateral" / "data" / \
        "suburb_irsd_irsad.csv"
    df = pd.read_csv(path)
    df["SUBURB_KEY"] = df["suburb_name"].apply(normalise_suburb_name)
    return df


crime_df = load_crime_data()
seifa_df = load_seifa_data()

irsd_table = load_irsd_scoring_table()
irsad_table = load_irsad_scoring_table()


# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Collateral Review",
    page_icon="🏠",
    layout="centered"
)


# =====================================================
# Header
# =====================================================
st.title("🏠 Collateral Review")
st.caption("Five C Credit Framework • Collateral • Prototype V1")
st.markdown("---")


# =====================================================
# Address Input
# =====================================================
st.subheader("📍 Property Address Information")

address_line = st.text_input("Street Address")
suburb = st.text_input("Suburb")
state = st.selectbox(
    "State / Territory",
    ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]
)
postcode = st.text_input("Postcode")

st.markdown("---")


# =====================================================
# Trigger Assessment
# =====================================================
if st.button("Continue to Collateral Assessment", use_container_width=True):
    if not all([address_line, suburb, postcode]):
        st.error("Please complete all required address fields.")
    else:
        st.session_state["run_collateral_assessment"] = True
        st.session_state["input_suburb"] = normalise_suburb_name(suburb)


# =====================================================
# Assessment Result
# =====================================================
if st.session_state["run_collateral_assessment"]:

    st.markdown("---")
    st.subheader("📊 Collateral Assessment Result")

    suburb_key = st.session_state["input_suburb"]

    crime_row = crime_df[crime_df["SUBURB_KEY"] == suburb_key]
    seifa_row = seifa_df[seifa_df["SUBURB_KEY"] == suburb_key]

    if crime_row.empty or seifa_row.empty:
        st.warning("Required suburb-level data not found.")
        st.stop()

    crime_percentile = float(crime_row.iloc[0]["crime_percentile"])
    crime_score = crime_score_from_percentile(crime_percentile)

    irsd_decile = int(seifa_row.iloc[0]["IRSD_decile"])
    irsad_decile = int(seifa_row.iloc[0]["IRSAD_decile"])

    irsd_score = irsd_table.loc[
        irsd_table["IRSD_Decile"] == irsd_decile, "Score"
    ].values[0]

    irsad_score = irsad_table.loc[
        irsad_table["IRSAD_Decile"] == irsad_decile, "Score"
    ].values[0]

    location_score = calculate_location_risk_score(
        crime_score, irsd_score, irsad_score
    )

    risk_label, risk_icon = classify_location_risk(location_score)

    # -------------------------------------------------
    # UI Output
    # -------------------------------------------------
    st.markdown("### 🏠 Property Summary")
    st.write(f"""
    **Address:** {address_line}  
    **Suburb:** {suburb.title()}  
    **State:** {state}  
    **Postcode:** {postcode}
    """)

    st.markdown("### 📍 Location Risk Indicators")

    c1, c2, c3 = st.columns(3)
    c1.metric("Crime Score", crime_score)
    c2.metric("IRSD Score", irsd_score)
    c3.metric("IRSAD Score", irsad_score)

    st.markdown("### 📌 Location Risk Summary")
    st.metric("Location Risk Score (V1)", location_score, delta=risk_label)

    if risk_icon == "🟢":
        st.success(f"{risk_icon} Overall location risk is **Low**.")
    elif risk_icon == "🟡":
        st.info(f"{risk_icon} Overall location risk is **Moderate**.")
    else:
        st.warning(f"{risk_icon} Overall location risk is **Elevated**.")

    st.markdown("### 🚓 Crime Safety")
    st.metric(
        "Crime Safety Percentile",
        f"{crime_percentile:.1f}%",
        help="Percentage of suburbs with higher crime rates"
    )


# =====================================================
# Disclaimer
# =====================================================
st.markdown("---")
st.caption(
    "Decision-support tool only. Not a substitute for formal credit assessment."
)
