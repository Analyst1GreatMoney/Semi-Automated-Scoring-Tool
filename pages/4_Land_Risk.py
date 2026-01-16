# =====================================================
# Imports
# =====================================================
import streamlit as st
import streamlit.components.v1 as components

from utils.session import init_session_state

# =====================================================
# Session Init
# =====================================================
init_session_state()

# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Land Risk Assessment",
    page_icon="🏞️",
    layout="centered",
)

# =====================================================
# Header
# =====================================================
st.title("🏞️ Land Risk Assessment")
st.caption("Collateral • Land Risk & Planning Constraints")

st.markdown("---")

# =====================================================
# Land Risk Lenses Overview
# =====================================================
st.subheader("🔎 Land Risk Lenses")

st.markdown(
    """
    | Valuer Lens | Core Question |
    |------------|---------------|
    | **Planning & Legal** | Is the land legally and planning-wise permitted for its intended use? |
    | **Title & Encumbrance** | Is the ownership clear and free from material encumbrances? |
    | **Environmental & Physical** | Are there physical or environmental constraints affecting usability or value? |
    | **Site Suitability** | Is the site practically usable and readily marketable? |
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# =====================================================
# Planning & Legal
# =====================================================
st.subheader("📐 Planning & Legal")
st.caption("Statutory, planning and legal constraints affecting land usability")

st.markdown("---")

# =====================================================
# Stubbed Planning & Legal Components
# (Later you will replace these with real policy logic)
# =====================================================
planning_components = {
    "Zoning Effect": {
        "score": 70,
        "label": "Low Risk",
        "rationale": (
            "<strong>Zoning Effect:</strong> Permitted for intended residential use<br>"
            "<strong>Overall:</strong> zoning planning risk assessed as <strong>low risk</strong>"
        ),
        "requires_manual_review": False,
    },
    "Overlays": {
        "score": 50,
        "label": "Moderate Risk",
        "rationale": (
            "<strong>Overlays:</strong> Overlay status not confirmed<br>"
            "<strong>Overall:</strong> planning overlay risk assessed as <strong>moderate risk</strong>"
        ),
        "requires_manual_review": True,
    },
    "Valuation Risk Alerts": {
        "score": 30,
        "label": "Elevated Risk",
        "rationale": (
            "<strong>Valuation alerts:</strong> Adverse planning comment noted<br>"
            "<strong>Overall:</strong> valuation legal risk assessed as <strong>elevated risk</strong>"
        ),
        "requires_manual_review": True,
    },
}

# =====================================================
# Planning & Legal Risk Breakdown (UI aligned with Neighbourhood)
# =====================================================
st.subheader("🔍 Planning & Legal Risk Breakdown")

html_rows = ""
manual_review_target = None

for name, comp in planning_components.items():

    score = comp.get("score")
    label = comp.get("label")
    rationale = comp.get("rationale")
    requires_manual_review = comp.get("requires_manual_review", False)

    # -----------------------------
    # Visual styles by risk label
    # -----------------------------
    if label == "Low Risk":
        bg = "#f3faf6"
        pill_bg = "#e6f4ea"
        pill_text = "#1b5e20"
        bar = "#2e7d32"
    elif label == "Moderate Risk":
        bg = "#fff8eb"
        pill_bg = "#fff1cc"
        pill_text = "#8d6e00"
        bar = "#f9a825"
    else:
        bg = "#fdecea"
        pill_bg = "#f9d6d5"
        pill_text = "#8e0000"
        bar = "#c62828"

    left_border = "none"
    badge_html = ""

    # -----------------------------
    # Manual review indicator
    # -----------------------------
    if requires_manual_review:
        left_border = f"6px solid {bar}"
        badge_html = """
        <span style="
            padding:2px 6px;
            border-radius:999px;
            font-size:0.7rem;
            font-weight:700;
            background:#fde68a;
            color:#92400e;
        ">
            ⚠ Manual Review
        </span>
        """

        manual_review_target = {
            "module": "Land Risk",
            "component": name,
            "original_score": score,
            "trigger": "Policy / Data Uncertainty",
        }

    html_rows += f"""
    <div style="
        display:grid;
        grid-template-columns: 1.6fr 0.6fr 1fr 2.4fr;
        column-gap:16px;
        padding:14px 16px;
        margin-bottom:10px;
        border-radius:10px;
        background:{bg};
        border-left:{left_border};
        align-items:start;
    ">
        <div style="font-weight:600;">{name}</div>

        <div style="font-weight:600;">
            {score}
        </div>

        <div>
            <span style="
                display:inline-block;
                padding:3px 10px;
                border-radius:999px;
                font-size:0.75rem;
                font-weight:700;
                background:{pill_bg};
                color:{pill_text};
            ">
                {label}
            </span>
        </div>

        <div style="font-size:0.85rem; line-height:1.6; color:#333;">
            {rationale}
            {badge_html}
        </div>
    </div>
    """

components.html(
    f"""
    <div style="margin-top:12px;">
        <div style="
            display:grid;
            grid-template-columns: 1.6fr 0.6fr 1fr 2.4fr;
            column-gap:16px;
            padding:6px 16px;
            margin-bottom:8px;
            font-size:0.72rem;
            font-weight:600;
            color:#6b7280;
            border-bottom:1px solid #e5e7eb;
            text-transform:uppercase;
            letter-spacing:0.06em;
        ">
            <div>Component</div>
            <div>Score</div>
            <isk Rating</div>
            <div>Key Drivers</div>
        </div>

        {html_rows}
    </div>
    """,
    height=420,
)

# =====================================================
# Manual Review CTA
# =====================================================
if manual_review_target:
    st.markdown("---")
    st.subheader("📝 Manual Review")

    st.info(
        "One or more land risk components require manual review "
        "under internal policy. A manual override may be requested."
    )

    if st.button("⚠️ Request Manual Review", use_container_width=True):
        st.session_state["manual_override"] = manual_review_target
        st.switch_page("pages/5_Manual_Review.py")

# =====================================================
# Navigation
# =====================================================
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Back to Neighbourhood Risk", use_container_width=True):
        st.switch_page("pages/3_Neighbourhood_Risk_Results.py")

with col2:
    if st.button("➡️ Continue to Improvements / Dwelling", use_container_width=True):
        st.switch_page("pages/5_Improvements_Risk.py")

# =====================================================
# Disclaimer
# =====================================================
st.markdown("---")
st.caption("Decision-support tool only. Not a substitute for formal credit assessment.")
