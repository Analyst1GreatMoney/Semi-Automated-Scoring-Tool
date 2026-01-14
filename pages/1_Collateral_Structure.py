import streamlit as st
from utils.session import init_session_state

# =====================================================
# Session Init
# =====================================================
init_session_state()

# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Collateral Risk Structure",
    page_icon="🏗️",
    layout="centered",
)

# =====================================================
# Header
# =====================================================
st.title("🏗️ Collateral Risk Structure")
st.caption("How collateral risk is assessed")
st.markdown("---")

# =====================================================
# Content
# =====================================================
st.markdown(
    """
    Collateral risk is assessed across two dimensions:
    """
)

st.markdown(
    """
    ### 🏘️ Neighbourhood Risk

    - Crime indicators  
    - Socio-economic indices (SEIFA)  
    - Zoning context  
    - Marketability & LGA considerations  
    """
)

st.markdown(
    """
    ### 🌍 Land Risk *(Planned)*

    - Planning overlays  
    - Permissibility & constraints  
    - Legal non-conformity  
    """
)

st.markdown("---")

# =====================================================
# Action
# =====================================================
if st.button(
    "Start Neighbourhood Risk Assessment",
    use_container_width=True,
):
    st.switch_page("pages/2_Neighbourhood_Risk.py")

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.caption(
    "Neighbourhood risk assessment is the first implemented module "
    "within the Collateral framework."
)