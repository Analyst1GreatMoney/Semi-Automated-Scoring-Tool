import streamlit as st

# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Home Page",
    page_icon="🏦",
    layout="centered"
)

# =====================================================
# Header
# =====================================================
st.title("🏦 Semi-Automated Credit Scoring Tool")
st.caption("Prototype Decision-Support System • Five C Credit Framework")
st.markdown("---")

# =====================================================
# Introduction
# =====================================================
st.markdown(
    """
    ### 👋 Welcome

    This application is a **semi-automated credit risk assessment prototype**
    built around the **Five C Credit Framework**:

    - **Character**
    - **Capacity**
    - **Capital**
    - **Collateral**
    - **Conditions**

    The tool is designed to support **credit analysts and lending teams**
    by combining structured data, policy-based scoring logic, and
    transparent risk indicators.

    ---
    """
)

# =====================================================
# Scope Highlight
# =====================================================
st.subheader("🔍 Current Scope (Prototype V1)")

st.markdown(
    """
    - 🏠 **Collateral – Location & Neighbourhood Risk**
        - Crime risk indicators
        - Socio-economic indices (IRSD / IRSAD)
        - Composite location risk scoring

    Additional Five C modules will be progressively integrated
    in future iterations.
    """
)

st.markdown("---")

# =====================================================
# Get Started Button
# =====================================================
if st.button("🚀 Get Started", use_container_width=True):
    # Streamlit built-in page navigation
    st.switch_page("pages/1_Collateral.py")

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.caption(
    "Decision-support tool only. Not a substitute for formal credit assessment."
)
