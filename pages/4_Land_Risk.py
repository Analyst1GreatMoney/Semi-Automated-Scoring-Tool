import streamlit as st

st.set_page_config(
    page_title="Land Risk Assessment",
    layout="centered"
)

# =====================================================
# Header
# =====================================================
st.title("🏗️ Land Risk Assessment")
st.caption("Collateral · Land Risk Factors")

st.markdown("---")

# =====================================================
# Planning & Legal
# =====================================================
st.subheader("📜 Planning & Legal")

# =====================================================
# Zoning Effect – Valuation Interpretation
# =====================================================
st.markdown("### 🏷️ Zoning Effect (Valuation Report)")

st.markdown(
    """
    <div style="
        background-color:#f8fafc;
        border:1px solid #e5e7eb;
        border-radius:12px;
        padding:16px 18px;
        margin-bottom:12px;
    ">
        <div style="font-size:13px; color:#374151; margin-bottom:6px;">
            Valuation Commentary
        </div>
        <div style="font-size:12px; color:#6b7280;">
            Summarise or paste the zoning-related assessment from the valuation report.  
            Focus on how zoning affects permissible use and development potential.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

zoning_effect_text = st.text_area(
    label="",
    placeholder=(
        "Example statements commonly used in valuation reports:\n\n"
        "• Residential use is permitted under current zoning.\n"
        "• Permitted subject to council consent or development approval.\n"
        "• Existing use rights apply; redevelopment may be constrained.\n"
        "• Planning controls significantly limit future development.\n"
        "• Use is non-conforming or prohibited under current zoning."
    ),
    height=180
)


# =====================================================
# Title & Encumbrance
# =====================================================
st.markdown("---")
st.subheader("📑 Title & Encumbrance")

col1, col2 = st.columns(2)

with col1:
    easements = st.selectbox(
        "Easements on Title",
        options=["None", "Minor", "Material", "Unknown"]
    )

    covenants = st.selectbox(
        "Restrictive Covenants",
        options=["None", "Minor", "Material", "Unknown"]
    )

with col2:
    strata_title = st.selectbox(
        "Strata / Community Title",
        options=["No", "Yes", "Unknown"]
    )

    title_irregularities = st.selectbox(
        "Title Irregularities",
        options=["No", "Yes", "Unknown"]
    )

# =====================================================
# Environmental & Physical
# =====================================================
st.markdown("---")
st.subheader("🌱 Environmental & Physical")

col1, col2 = st.columns(2)

with col1:
    contamination_risk = st.selectbox(
        "Contamination Risk",
        options=["Low", "Moderate", "High", "Unknown"]
    )

    slope_condition = st.selectbox(
        "Land Slope",
        options=["Flat", "Moderate Slope", "Steep", "Unknown"]
    )

with col2:
    flooding_history = st.selectbox(
        "Historical Flooding",
        options=["No", "Yes", "Unknown"]
    )

    soil_stability = st.selectbox(
        "Soil Stability",
        options=["Stable", "Variable", "Unstable", "Unknown"]
    )

# =====================================================
# Site Suitability
# =====================================================
st.markdown("---")
st.subheader("📐 Site Suitability")

col1, col2 = st.columns(2)

with col1:
    site_access = st.selectbox(
        "Site Access",
        options=["Good", "Restricted", "Poor"]
    )

    servicing = st.selectbox(
        "Utility Servicing",
        options=["Fully Serviced", "Partially Serviced", "Unserviced"]
    )

with col2:
    shape_efficiency = st.selectbox(
        "Lot Shape Efficiency",
        options=["Regular", "Irregular", "Highly Constrained"]
    )

    development_constraints = st.selectbox(
        "Overall Development Constraints",
        options=["Low", "Moderate", "High"]
    )

# =====================================================
# Action
# =====================================================
st.markdown("---")

if st.button("▶️ Run Land Risk Assessment", use_container_width=True):
    st.success("Land risk inputs captured. Ready for assessment logic.")