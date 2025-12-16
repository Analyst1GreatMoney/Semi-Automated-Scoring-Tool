import streamlit as st

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Collateral Review",
    page_icon="🏠",
    layout="centered"
)

# =========================
# Header
# =========================
st.title("🏠 Collateral Review")
st.caption(
    "Five C Framework • Component 1: Collateral • Prototype V1"
)

st.markdown("---")

# =========================
# Intro
# =========================
st.markdown(
    """
This section focuses on **reviewing the property offered as collateral**
for the proposed loan.

Please provide the **basic property address details** below.
These inputs will be used in later stages to support
risk assessment and collateral scoring.
"""
)

# =========================
# Address Input Section
# =========================
st.subheader("📍 Property Address Information")

address_line = st.text_input(
    "Street Address",
    placeholder="e.g. 123 George Street"
)

suburb = st.text_input(
    "Suburb",
    placeholder="e.g. Sydney"
)

state = st.selectbox(
    "State / Territory",
    ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]
)

postcode = st.text_input(
    "Postcode",
    placeholder="e.g. 2000"
)

# =========================
# Validation & Continue
# =========================
st.markdown("---")

if st.button("Continue to Collateral Assessment", use_container_width=True):
    if not all([address_line, suburb, postcode]):
        st.error("Please complete all required address fields before proceeding.")
    else:
        st.success("Address captured successfully. Collateral assessment logic will be applied next.")
