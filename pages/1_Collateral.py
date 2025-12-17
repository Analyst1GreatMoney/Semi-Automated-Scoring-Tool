# =====================================================
# Imports
# =====================================================
import streamlit as st
from utils.session import init_session_state

from utils.paths import BASE_DIR, DATA_DIR
from data.normalisation import normalise_suburb_name

from data.location import get_location_datasets

from policies.location import assess_location_risk
from policies.zoning import assess_zoning_risk
from policies.lga import assess_lga_risk
from policies.marketability import assess_marketability_risk

from engine.composite import compute_location_neighbourhood_score
from engine.classification import classify_composite_location_risk

init_session_state()

# -----------------------------------------------------
# Session State Initialization (VERY IMPORTANT)
# -----------------------------------------------------
if "input_suburb" not in st.session_state:
    st.session_state["input_suburb"] = ""

if "input_lga" not in st.session_state:
    st.session_state["input_lga"] = ""

if "marketability" not in st.session_state:
    st.session_state["marketability"] = None


# =====================================================
# Data Layer (read-only for page)
# =====================================================
datasets = get_location_datasets()
crime_df = datasets["crime"]
seifa_df = datasets["seifa"]
lga_irsad_df = datasets["lga_irsad"]


# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Collateral Review",
    page_icon="🏠",
    layout="centered",
)


# =====================================================
# UI – Header
# =====================================================
st.title("🏠 Collateral Review")
st.caption("Five C Credit Framework • Collateral • Prototype V1.1")
st.markdown("---")


# =====================================================
# UI – Property Address
# =====================================================
st.subheader("📍 Property Address Information")

address_line = st.text_input("Street Address")
suburb = st.text_input("Suburb")
state = st.selectbox(
    "State / Territory",
    ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"],
)
postcode = st.text_input("Postcode")

st.markdown("---")


# =====================================================
# UI – Zoning
# =====================================================
st.subheader("🏗️ Zoning Information")

zoning_options = [
    "R1 General Residential",
    "R2 Low Density Residential",
    "R3 Medium Density Residential",
    "R4 High Density Residential",
    "R5 Large Lot Residential",
    "Other",
]

selected_zoning = st.selectbox("Zoning Classification", zoning_options)

# Policy warning (UI responsibility)
if selected_zoning == "R4 High Density Residential":
    st.warning(
        """
        **High Density Residential Policy Notice**

        High-density apartments may be subject to additional credit restrictions, including
        minimum dwelling size, external sales evidence requirements, and enhanced serviceability
        assessment. Certain applications may require senior credit approval.
        """,
        icon="⚠️",
    )

custom_zoning = None
if selected_zoning == "Other":
    custom_zoning = st.text_input(
        "Specify zoning code (max 3 characters)",
        max_chars=3,
    )

zoning_value = (
    custom_zoning.strip().upper()
    if selected_zoning == "Other" and custom_zoning
    else selected_zoning.split(" ")[0]
)

st.markdown("---")


# =====================================================
# UI – LGA
# =====================================================
st.subheader("🏛️ Local Government Area (LGA)")

lga = st.text_input(
    "Local Government Area",
    help="e.g. City of Sydney, Parramatta City Council",
)

st.markdown("---")


# =====================================================
# UI – Marketability
# =====================================================
st.subheader("📈 Marketability")

marketability_options = ["Very Good", "Good", "Average", "Fair", "Poor"]

selected_marketability = st.selectbox(
    "Marketability Assessment",
    marketability_options,
    help="Indicative resale demand based on valuation commentary",
)

marketability_value = selected_marketability.upper()


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
    st.markdown("# 📊 Collateral Assessment Result")

    suburb_key = st.session_state.get("input_suburb", "")

    # -------------------------------------------------
    # Crime data (defensive)
    # -------------------------------------------------
    crime_row = None
    if not crime_df.empty and "SUBURB_KEY" in crime_df.columns:
        filtered = crime_df[crime_df["SUBURB_KEY"] == suburb_key]
        if not filtered.empty:
            crime_row = filtered.iloc[0]

    # -------------------------------------------------
    # SEIFA data (defensive)
    # -------------------------------------------------
    seifa_row = None
    if not seifa_df.empty and "SUBURB_KEY" in seifa_df.columns:
        filtered = seifa_df[seifa_df["SUBURB_KEY"] == suburb_key]
        if not filtered.empty:
            seifa_row = filtered.iloc[0]

    # -------------------------------------------------
    # Guard: required suburb-level data
    # -------------------------------------------------
    if crime_row is None or seifa_row is None:
        st.warning("Suburb-level crime or SEIFA data not available. Assessment completed with limited inputs.")

    # -------------------------------------------------
    # Policy Assessments
    # -------------------------------------------------
    location_result = assess_location_risk(
        crime_percentile=float(crime_row["crime_percentile"]) if crime_row is not None else None,
        irsd_decile=int(seifa_row["IRSD_decile"]) if seifa_row is not None else None,
        irsad_decile=int(seifa_row["IRSAD_decile"]) if seifa_row is not None else None,
    )

    zoning_result = assess_zoning_risk(zoning_value)
    lga_result = assess_lga_risk(lga)
    marketability_result = assess_marketability_risk(marketability_value)

    # -------------------------------------------------
    # Composite Score
    # -------------------------------------------------
    location_neighbourhood_score = compute_location_neighbourhood_score(
        results=[
            location_result,
            zoning_result,
            lga_result,
            marketability_result,
        ]
    )

    final_label, final_icon = classify_composite_location_risk(
        location_neighbourhood_score
    )


    # -------------------------------------------------
    # Policy Assessments
    # -------------------------------------------------
    location_result = assess_location_risk(
        crime_percentile=float(crime_row.iloc[0]["crime_percentile"]),
        irsd_decile=int(seifa_row.iloc[0]["IRSD_decile"]),
        irsad_decile=int(seifa_row.iloc[0]["IRSAD_decile"]),
    )

    zoning_result = assess_zoning_risk(zoning_value)
    lga_result = assess_lga_risk(lga)
    marketability_result = assess_marketability_risk(marketability_value)

    # -------------------------------------------------
    # Composite Location / Neighbourhood Score
    # -------------------------------------------------
    location_neighbourhood_score = compute_location_neighbourhood_score(
        results=[
            location_result,
            zoning_result,
            lga_result,
            marketability_result,
        ]
    )

    final_label, final_icon = classify_composite_location_risk(
        location_neighbourhood_score
    )

    # =================================================
    # UI – Output
    # =================================================
    st.markdown("#### 🏠 Property Summary")
    st.markdown(
        f"""
        **Address:** {address_line}  
        **Suburb:** {suburb.title()}  
        **State:** {state}  
        **Postcode:** {postcode}  

        **Zoning:** {zoning_value or "Not specified"}  
        **Local Government Area (LGA):** {lga or "Not specified"}  
        **Marketability:** {marketability_value.title()}
        """
    )

    st.markdown("## 📌 Location / Neighbourhood Risk")

    st.metric(
        "Overall Location & Neighbourhood Risk Score",
        f"{final_icon} {location_neighbourhood_score}",
        help="Composite score derived from location, zoning, LGA socio-economic profile and marketability.",
    )

    st.caption(f"{final_label} — classification based on composite scoring.")


# =====================================================
# Disclaimer
# =====================================================
st.markdown("---")
st.caption(
    "Decision-support tool only. Not a substitute for formal credit assessment."
)
