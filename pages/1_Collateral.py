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
# pages/1_Collateral.py
# =====================================================
BASE_DIR = Path(__file__).resolve().parents[1]


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

def normalise_lga_name(name: str) -> str:
    """
    Normalise LGA names for robust matching between:
    - Valuation reports (e.g. 'The Hills Shire Council')
    - ABS / IRSAD datasets (e.g. 'The Hills Shire')

    Strategy:
    - Uppercase
    - Remove state suffixes
    - Remove common administrative words (COUNCIL, CITY OF)
    - Normalise whitespace
    """

    if not name:
        return ""

    cleaned = (
        name.upper()
        .replace("(NSW)", "")
        .replace("(VIC)", "")
        .replace("(QLD)", "")
        .replace("(WA)", "")
        .replace("(SA)", "")
        .replace("(TAS)", "")
        .replace("(ACT)", "")
        .replace("(NT)", "")
        .replace("COUNCIL", "")
        .replace("CITY OF", "")
        .replace("CITY", "")   # optional but practical
        .strip()
    )

    # Collapse multiple spaces into one
    cleaned = " ".join(cleaned.split())

    return cleaned


# =====================================================
# Policy Layer – Location Scoring
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
# Policy Layer – Zoning Scoring (Hidden from UI)
# =====================================================
def load_residential_zoning_scoring_table():
    return pd.DataFrame({
        "Zoning Code": ["R1", "R2", "R3", "R4", "R5"],
        "Score": [65, 80, 55, 30, 50]
    })


def load_non_residential_zoning_scoring_table():
    return pd.DataFrame({
        "Zoning Code": [
            "RU1","RU2","RU3","RU4","RU5","RU6",
            "B1","B2","B3","B4","B5","B6","B7","B8",
            "IN1","IN2","IN3","IN4",
            "SP1","SP2","SP3",
            "RE1","RE2",
            "E1","E2","E3","E4",
            "W1","W2","W3"
        ],
        "Score": [
            10,15,5,20,60,25,
            40,35,15,30,10,10,5,20,
            5,10,0,0,
            5,0,20,
            5,15,
            0,5,15,45,
            0,5,0
        ]
    })


def resolve_zoning_risk(zoning_code: str):
    """
    Backend-only zoning risk resolution.
    Returns: (risk_label, icon, explanation)
    """

    if zoning_code is None:
        return "Unknown", "⚪", "Zoning information was not provided."

    zoning_code = zoning_code.upper().strip()

    res_df = load_residential_zoning_scoring_table()
    non_res_df = load_non_residential_zoning_scoring_table()

    if zoning_code in res_df["Zoning Code"].values:
        score = int(res_df.loc[
            res_df["Zoning Code"] == zoning_code, "Score"
        ].values[0])

        if score >= 70:
            return "Low Risk", "🟢", "Residential zoning with strong market acceptance."
        elif score >= 50:
            return "Moderate Risk", "🟡", "Residential zoning with standard development constraints."
        else:
            return "Elevated Risk", "🔴", "Residential zoning with reduced market liquidity."

    if zoning_code in non_res_df["Zoning Code"].values:
        score = int(non_res_df.loc[
            non_res_df["Zoning Code"] == zoning_code, "Score"
        ].values[0])

        if score >= 40:
            return "Moderate Risk", "🟡", "Non-residential zoning with adaptive or mixed-use potential."
        elif score > 0:
            return "Elevated Risk", "🔴", "Specialised zoning with limited residential demand."
        else:
            return "High Risk", "🔴", "Highly restrictive zoning with low collateral liquidity."

    return "High Risk", "🔴", "Unclassified zoning with uncertain planning risk."

def resolve_lga_irsad_risk(lga_name: str):
    """
    Resolve LGA-level IRSAD risk from user input.
    Returns: (risk_label, icon, explanation)
    """

    if not lga_name:
        return "Unknown", "⚪", "Local Government Area not provided."

    lga_key = normalise_lga_name(lga_name)

    match = lga_irsad_df[lga_irsad_df["LGA_KEY"] == lga_key]

    if match.empty:
        return "Unknown", "⚪", "LGA not found in socio-economic database."

    irsad_decile = int(match.iloc[0]["IRSAD_decile"])

    # Reuse IRSAD decile logic (hidden from UI)
    if irsad_decile >= 8:
        return "Low Risk", "🟢", "LGA shows strong socio-economic advantage."
    elif irsad_decile >= 5:
        return "Moderate Risk", "🟡", "LGA shows average socio-economic conditions."
    else:
        return "Elevated Risk", "🔴", "LGA shows relative socio-economic disadvantage."

# =====================================================
# Data Layer
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

@st.cache_data
def load_lga_irsad_data():
    """
    Load LGA-level IRSAD data (2021)
    """
    path = BASE_DIR / "doc" / "Collateral" / "data" / "lga_irsad_2021_clean.csv"
    df = pd.read_csv(path)

    # Normalise LGA names for matching
    df["LGA_KEY"] = df["lga_name"].apply(normalise_lga_name)

    return df

crime_df = load_crime_data()
seifa_df = load_seifa_data()
lga_irsad_df = load_lga_irsad_data()

# =====================================================
# Initialise Scoring Tables (Global)
# =====================================================
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
# UI – Header
# =====================================================
st.title("🏠 Collateral Review")
st.caption("Five C Credit Framework • Collateral • Prototype V1.1")
st.markdown("---")


# =====================================================
# UI – Address Input
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
# UI – Zoning Input
# =====================================================
st.subheader("🏗️ Zoning Information")

zoning_options = [
    "R1 General Residential",
    "R2 Low Density Residential",
    "R3 Medium Density Residential",
    "R4 High Density Residential",
    "R5 Large Lot Residential",
    "Other"
]

selected_zoning = st.selectbox(
    "Zoning Classification",
    zoning_options
)

custom_zoning = None
if selected_zoning == "Other":
    custom_zoning = st.text_input(
        "Specify zoning code (max 3 characters)",
        max_chars=3
    )

zoning_value = (
    custom_zoning.strip().upper()
    if selected_zoning == "Other" and custom_zoning
    else selected_zoning.split(" ")[0]
)

# =====================================================
# UI – Local Government Area (LGA)
# =====================================================
st.subheader("🏛️ Local Government Area (LGA)")

lga = st.text_input(
    "Local Government Area",
    help="Enter the Local Government Area (e.g. City of Sydney, Parramatta City Council)"
)

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

    # -------------------------------------------------
    # Suburb-level Risk (Crime + SEIFA)
    # -------------------------------------------------
    crime_score = crime_score_from_percentile(
        float(crime_row.iloc[0]["crime_percentile"])
    )

    irsd_score = irsd_table.loc[
        irsd_table["IRSD_Decile"] == int(seifa_row.iloc[0]["IRSD_decile"]),
        "Score"
    ].values[0]

    irsad_score = irsad_table.loc[
        irsad_table["IRSAD_Decile"] == int(seifa_row.iloc[0]["IRSAD_decile"]),
        "Score"
    ].values[0]

    location_score = calculate_location_risk_score(
        crime_score, irsd_score, irsad_score
    )

    location_label, location_icon = classify_location_risk(location_score)

    # -------------------------------------------------
    # Zoning Risk (Planning)
    # -------------------------------------------------
    zoning_label, zoning_icon, zoning_explanation = resolve_zoning_risk(zoning_value)

    # -------------------------------------------------
    # LGA IRSAD Risk (Macro Socio-economic)
    # -------------------------------------------------
    lga_label, lga_icon, lga_explanation = resolve_lga_irsad_risk(lga)

    # =================================================
    # UI – Output
    # =================================================
    st.markdown("### 🏠 Property Summary")
    st.write(f"""
    **Address:** {address_line}  
    **Suburb:** {suburb.title()}  
    **State:** {state}  
    **Postcode:** {postcode}  
    **Local Government Area:** {lga if lga else "Not specified"}
    """)

    # -------------------------------------------------
    # Location Risk Summary
    # -------------------------------------------------
    st.markdown("### 📍 Location Risk Summary")
    st.metric(
        "Overall Location Risk",
        f"{location_icon} {location_label}"
    )

    # -------------------------------------------------
    # Zoning Risk Output
    # -------------------------------------------------
    st.markdown("### 🏗️ Zoning Risk Assessment")
    st.markdown(
        f"""
        **Zoning:** {zoning_value if zoning_value else "Not specified"}  
        **Risk Level:** {zoning_icon} **{zoning_label}**

        _{zoning_explanation}_
        """
    )

    # -------------------------------------------------
    # LGA Socio-Economic Risk Output
    # -------------------------------------------------
    st.markdown("### 🏛️ LGA Socio-Economic Risk")
    st.markdown(
        f"""
        **LGA:** {lga if lga else "Not specified"}  
        **Risk Level:** {lga_icon} **{lga_label}**

        _{lga_explanation}_
        """
    )


# =====================================================
# Disclaimer
# =====================================================
st.markdown("---")
st.caption(
    "Decision-support tool only. Not a substitute for formal credit assessment."
)
