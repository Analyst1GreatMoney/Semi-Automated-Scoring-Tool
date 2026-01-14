import streamlit as st
from utils.session import init_session_state

# =====================================================
# Session Init
# =====================================================
init_session_state()

# =====================================================
# Header
# =====================================================
st.title("📊 Neighbourhood Risk Assessment Report")
st.caption("Collateral • Location & Neighbourhood Risk")
st.markdown("---")

# =====================================================
# Load Result
# =====================================================
result = st.session_state.get("neighbourhood_result")

if not result:
    st.error("No neighbourhood risk assessment found.")
    st.stop()

summary = result["summary"]
components = result["components"]

# =====================================================
# 1️⃣ Property Summary
# =====================================================
st.subheader("🏠 Property Summary")

st.markdown(
    f"""
    **Address:** {summary["address"]}  
    **Suburb:** {summary["suburb"].title()}  
    **State:** {summary["state"]}  
    **Postcode:** {summary["postcode"]}  

    **Zoning:** {summary["zoning"]}  
    **Local Government Area (LGA):** {summary["lga"] or "Not specified"}  
    **Marketability:** {summary["marketability"].title()}
    """
)

# =====================================================
# 2️⃣ Composite Risk Summary
# =====================================================
st.markdown("---")
st.subheader("📌 Composite Neighbourhood Risk Summary")

st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background-color: {result["icon"]};
        "></div>
        <div style="font-size: 36px; font-weight: 600;">
            {result["score"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(f"**Risk Classification:** {result['label']}")

st.caption(
    "The composite neighbourhood risk score reflects an aggregated assessment "
    "of location, zoning, local government area, and marketability factors."
)

# =====================================================
# 3️⃣ Zoning Policy Consideration
# =====================================================
st.markdown("---")
st.subheader("🏗️ Zoning Policy Consideration")

zoning = summary["zoning"]

if zoning == "R4":
    st.markdown(
        """
        The subject property is located within a **High Density Residential (R4)** zone.

        From a credit risk perspective, high-density zoning may introduce additional
        considerations related to:
        - Apartment supply concentration  
        - Market liquidity and resale depth  
        - Sensitivity to broader residential market cycles  

        While R4 zoning does not imply adverse credit risk in isolation, it is typically
        subject to **enhanced review within collateral assessment frameworks**.
        """
    )
else:
    st.markdown(
        """
        The subject property is located within a standard residential zoning category.
        Residential zoning generally supports stable market demand, subject to
        location-specific and marketability considerations.
        """
    )

# =====================================================
# 4️⃣ Risk Component Breakdown
# =====================================================
st.markdown("---")
st.subheader("🔍 Risk Component Breakdown")

st.caption(
    "The following section outlines the contribution of each risk component "
    "to the overall neighbourhood risk score."
)

def render_component(name, component):
    st.markdown(f"### {name} Risk")

    score = component.get("score", "N/A")
    label = component.get("label", "N/A")
    rationale = component.get("rationale")

    st.markdown(
        f"""
        **Score:** {score}  
        **Risk Level:** {label}
        """
    )

    if rationale:
        st.markdown(
            f"""
            **Assessment Rationale:**  
            {rationale}
            """
        )
    else:
        st.caption("No additional qualitative commentary provided.")

for key, component in components.items():
    render_component(key.title(), component)

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.caption(
    "This neighbourhood risk assessment is intended to support structured "
    "credit decision-making and does not replace formal valuation or lending judgement."
)