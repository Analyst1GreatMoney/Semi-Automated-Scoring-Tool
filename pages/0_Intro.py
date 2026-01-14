import streamlit as st
from utils.session import init_session_state

init_session_state()

st.title("🏠 Collateral Assessment")
st.caption("Five C Credit Framework • Collateral • Overview")
st.markdown("---")

st.markdown("""
### Why start with Collateral?

Collateral assessment provides a **downside-risk anchor** for credit decisions.

In early-stage screening, collateral helps:
- Establish minimum recovery expectations
- Identify location- or land-related red flags
- Support structured, explainable credit judgement
""")

st.markdown("""
### Current Scope (Prototype V1.1)

- ✅ Location & Neighbourhood Risk
- 🚧 Land Risk (planning, zoning overlays – upcoming)
""")

if st.button("Continue to Collateral Structure", use_container_width=True):
    st.switch_page("pages/1_Collateral_Structure.py")
