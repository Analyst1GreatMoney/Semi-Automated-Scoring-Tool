# =====================================================
# Imports
# =====================================================
import streamlit as st
from utils.session import init_session_state
from data.normalisation import normalise_suburb_name

from data.location import (
    get_location_datasets,
    get_location_inputs,
)

from policies.location import assess_location_risk
from policies.zoning import assess_zoning_risk
from policies.lga import assess_lga_risk
from policies.marketability import assess_marketability_risk

from engine.composite import compute_location_neighbourhood_score
from engine.classification import classify_composite_location_risk


# =====================================================
# Session Init
# =====================================================
init_session_state()

st.session_state.setdefault("neighbourhood_result", None)


# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Neighbourhood Risk Assessment",
    page_icon="🏘️",
    layout="centered",
)


# =====================================================
# Load Data
# =====================================================
datasets = get_location_datasets()


# =====================================================
# Header
# =====================================================
st.title("🏘️ Neighbourhood Risk Assessment")
st.caption("Collateral • Location & Neighbourhood Risk")

if st.button("← Back to Collateral Structure"):
    st.switch_page("pages/1_Collateral_Structure.py")

st.markdown("---")


# =====================================================
# Property Information
# =====================================================
st.subheader("📍 Property Address")

address_line = st.text_input("Street Address")
suburb = st.text_input("Suburb")
state = st.selectbox(
    "State / Territory",
    ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"],
)
postcode = st.text_input("Postcode")

st.markdown("---")


# =====================================================
# Zoning
# =====================================================
st.subheader("🏗️ Zoning")

zoning_options = [
    "R1 General Residential",
    "R2 Low Density Residential",
    "R3 Medium Density Residential",
    "R4 High Density Residential",
    "R5 Large Lot Residential",
    "Other",
]

selected_zoning = st.selectbox("Zoning Classification", zoning_options)

if selected_zoning == "R4 High Density Residential":
    st.markdown(
        """
        <div style="
            background-color: #fff8e1;
            border-left: 4px solid #f5c542;
            padding: 12px 14px;
            margin-top: 8px;
            display: flex;
            align-items: flex-start;
            gap: 10px;
            font-size: 0.9rem;
            color: #5c4b00;
        ">
            <div style="font-size: 1.1rem;">⚠️</div>
            <div>
                <strong>Policy warning:</strong>
                High-density residential zoning may be subject to additional credit
                considerations, including dwelling size and market liquidity constraints.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
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
# LGA
# =====================================================
st.subheader("🏛️ Local Government Area (LGA)")

lga = st.text_input(
    "Local Government Area",
    help="e.g. City of Sydney, Parramatta City Council",
)

st.markdown("---")


# =====================================================
# Marketability
# =====================================================
st.subheader("📈 Marketability")

marketability_options = ["Very Good", "Good", "Average", "Fair", "Poor"]
marketability_value = st.selectbox(
    "Marketability Assessment",
    marketability_options,
).upper()


# =====================================================
# Automatic Assessment (Silent)
# =====================================================
if all([address_line, suburb, postcode]):

    suburb_key = normalise_suburb_name(suburb)

    location_inputs = get_location_inputs(datasets, suburb_key)
    crime_row = location_inputs.get("crime")
    seifa_row = location_inputs.get("seifa")

    location_result = assess_location_risk(
        crime_percentile=float(crime_row["crime_percentile"]) if crime_row else None,
        irsd_decile=int(seifa_row["IRSD_decile"]) if seifa_row else None,
        irsad_decile=int(seifa_row["IRSAD_decile"]) if seifa_row else None,
    )

    zoning_result = assess_zoning_risk(zoning_value)
    lga_result = assess_lga_risk(lga)
    marketability_result = assess_marketability_risk(marketability_value)

    score = compute_location_neighbourhood_score(
        results=[
            location_result,
            zoning_result,
            lga_result,
            marketability_result,
        ]
    )

    label, icon = classify_composite_location_risk(score)

    st.session_state["neighbourhood_result"] = {
        "score": score,
        "label": label,
        "icon": icon,
        "components": {
            "location": location_result,
            "zoning": zoning_result,
            "lga": lga_result,
            "marketability": marketability_result,
        },
        "summary": {
            "address": address_line,
            "suburb": suburb,
            "state": state,
            "postcode": postcode,
            "zoning": zoning_value,
            "lga": lga,
            "marketability": marketability_value,
        },
    }


# =====================================================
# Next Step (Always at Bottom)
# =====================================================
col1, col2 = st.columns(2)

with col1:
    if st.button(
        "📊 Show Detailed Neighbourhood Risk Results",
        use_container_width=True,
    ):
        st.switch_page("pages/3_Neighbourhood_Risk_Results.py")

with col2:
    if st.button(
        "➡️ Continue to Land Risk Assessment",
        use_container_width=True,
    ):
        st.switch_page("pages/4_Land_Risk.py")


# =====================================================
# Disclaimer
# =====================================================
st.markdown("---")
st.caption(
    "Decision-support tool only. Not a substitute for formal credit assessment."
)
