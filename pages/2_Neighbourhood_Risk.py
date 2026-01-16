# =====================================================
# Imports
# =====================================================
import streamlit as st

from utils.session import init_session_state
from data.normalisation import (
    normalise_suburb_name,
    normalise_lga_name,
)

from data.loaders import get_location_datasets
from data.location import get_location_inputs

from policies.location import assess_location_risk
from policies.narratives.location_narrative import build_location_narrative
from policies.zoning import assess_zoning_risk
from policies.lga import assess_lga_risk
from policies.marketability import assess_marketability_risk
from policies.narratives.zoning_narrative import build_zoning_narrative
from policies.narratives.lga_narrative import build_lga_narrative
from policies.narratives.marketability_narrative import build_marketability_narrative

from engine.composite import compute_location_neighbourhood_score
from engine.classification import classify_composite_location_risk


# =====================================================
# Session Init
# =====================================================
init_session_state()


# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Neighbourhood Risk Assessment",
    page_icon="🏘️",
    layout="centered",
)


# =====================================================
# Load Data (cached)
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

# ⚠️ R4 policy warning（UI-only, 保留）
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

marketability_display = st.selectbox(
    "Marketability Assessment",
    ["Very Good", "Good", "Average", "Fair", "Poor"],
)

MARKETABILITY_MAP = {
    "Very Good": "VERY_GOOD",
    "Good": "GOOD",
    "Average": "AVERAGE",
    "Fair": "FAIR",
    "Poor": "POOR",
}

marketability_key = MARKETABILITY_MAP[marketability_display]

# =====================================================
# Automatic Assessment
# =====================================================
if all([address_line, suburb, postcode]):

    # -------- Input signature（防止无脑清 session）--------
    input_signature = (
        address_line.strip(),
        suburb.strip(),
        postcode.strip(),
        zoning_value,
        lga.strip() if lga else "",
        marketability_key,
    )

    if st.session_state.get("_last_neighbourhood_input") != input_signature:
        st.session_state.pop("neighbourhood_result", None)
        st.session_state["_last_neighbourhood_input"] = input_signature

    # -------- Normalised keys --------
    suburb_key = normalise_suburb_name(suburb)
    lga_key = normalise_lga_name(lga) if lga else None

    # -------- Fetch raw rows --------
    location_inputs = get_location_inputs(
        datasets,
        suburb_key=suburb_key,
        lga_key=lga_key,
    )

    crime_row = location_inputs.get("crime")
    seifa_row = location_inputs.get("seifa")

    # -------- Extract indicators --------
    crime_percentile = (
        float(crime_row["crime_percentile"])
        if crime_row is not None and "crime_percentile" in crime_row
        else None
    )

    irsd_decile = (
        int(seifa_row["IRSD_decile"])
        if seifa_row is not None and "IRSD_decile" in seifa_row
        else None
    )

    irsad_decile = (
        int(seifa_row["IRSAD_decile"])
        if seifa_row is not None and "IRSAD_decile" in seifa_row
        else None
    )

    # -------- Location assessment --------
    location_result = assess_location_risk(
        crime_percentile=crime_percentile,
        irsd_decile=irsd_decile,
        irsad_decile=irsad_decile,
    )

    location_result["rationale"] = build_location_narrative(
        crime_percentile=crime_percentile,
        irsd_decile=irsd_decile,
        irsad_decile=irsad_decile,
        final_score=location_result["score"],
        final_label=location_result["label"],
    )

    # -------- Other components --------
    zoning_result = assess_zoning_risk(zoning_value)

    zoning_result["rationale"] = build_zoning_narrative(
        zoning_code=zoning_result.get("zoning_code"),
        label=zoning_result.get("label"),
    )

    lga_result = assess_lga_risk(lga_key)

    lga_result["rationale"] = build_lga_narrative(
        lga_name=lga,
        label=lga_result.get("label"),
    )

    marketability_result = assess_marketability_risk(marketability_key)

    marketability_result["rationale"] = build_marketability_narrative(
        marketability_label=marketability_display,
        label=marketability_result.get("label"),
    )


    # -------- Composite score --------
    composite_score = round(
        compute_location_neighbourhood_score(
            results=[
                location_result,
                zoning_result,
                lga_result,
                marketability_result,
            ]
        ),
        1,
    )

    composite_label, composite_icon = classify_composite_location_risk(
        composite_score
    )

    # -------- Persist to session --------
    st.session_state["neighbourhood_result"] = {
        "score": composite_score,
        "label": composite_label,
        "icon": composite_icon,
        "summary": {
            "address": address_line,
            "suburb": suburb,
            "state": state,
            "postcode": postcode,
            "zoning": zoning_value,
            "lga": lga,
            "marketability": marketability_display,
        },
        "components": {
            "Location": {
                "score": location_result["score"],
                "label": location_result["label"],
                "rationale": location_result["rationale"],
            },
            "Zoning": zoning_result,
            "Lga": lga_result,
            "Marketability": marketability_result,
        },
    }


# =====================================================
# Navigation
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