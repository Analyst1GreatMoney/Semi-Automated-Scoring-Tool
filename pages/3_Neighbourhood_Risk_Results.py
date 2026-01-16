# =====================================================
# Imports
# =====================================================
import streamlit as st
import streamlit.components.v1 as components
import html

from utils.session import init_session_state
from policies.zoning import ZONING_POLICY_REGISTRY

# =====================================================
# Session Init
# =====================================================
init_session_state()

# =====================================================
# Page Config
# =====================================================
st.set_page_config(
    page_title="Neighbourhood Risk Results",
    page_icon="📊",
    layout="centered",
)

# =====================================================
# Load Result from Session
# =====================================================
result = st.session_state.get("neighbourhood_result")

if not result:
    st.error("No neighbourhood risk assessment found.")
    st.stop()

summary = result.get("summary", {})
components_data = result.get("components", {})

# ✅ 加这一行（必须在最前面定义）
applied_overrides = st.session_state.get("applied_overrides", {})

# =====================================================
# Header
# =====================================================
st.title("📊 Neighbourhood Risk Results")
st.caption("Collateral • Detailed Location & Neighbourhood Assessment")
st.markdown("---")

# =====================================================
# Property Summary
# =====================================================
st.subheader("🏠 Property Summary")

st.markdown(
    f"""
    **Address:** {summary.get("address", "—")}  
    **Suburb:** {summary.get("suburb", "—")}  
    **State:** {summary.get("state", "—")}  
    **Postcode:** {summary.get("postcode", "—")}  

    **Zoning:** {summary.get("zoning", "—")}  
    **Local Government Area (LGA):** {summary.get("lga", "—")}  
    **Marketability:** {summary.get("marketability", "—")}
    """
)

st.markdown("---")

# -------------------------------------------------
# Recalculate composite score using overridden values
# -------------------------------------------------
component_scores = []

for name, comp in components_data.items():
    base_score = comp.get("score")

    if name in applied_overrides:
        base_score = applied_overrides[name]["adjusted_score"]

    if base_score is not None:
        component_scores.append(base_score)

if component_scores:
    score = round(sum(component_scores) / len(component_scores), 1)

# =====================================================
# Composite Neighbourhood Risk
# =====================================================
st.subheader("📌 Neighbourhood Risk")

# ❌ 不要再用 result.get("score")
# score = result.get("score")

# ✅ 用 override 后重新算的 score
final_score = score

# 根据 final_score 动态算 label
if final_score >= 70:
    label = "Low Risk"
elif final_score >= 50:
    label = "Moderate Risk"
else:
    label = "Elevated Risk"

if label == "Low Risk":
    bg, bar, text = "#f1f8f4", "#2e7d32", "#2e7d32"
elif label == "Moderate Risk":
    bg, bar, text = "#fff6e0", "#f9a825", "#f57f17"
else:
    bg, bar, text = "#fdecea", "#c62828", "#c62828"

components.html(
    f"""
    <div style="
        display:flex;
        align-items:center;
        gap:24px;
        padding:20px;
        margin-top:12px;
        border-radius:12px;
        background:{bg};
        border-left:8px solid {bar};
    ">
        <div style="
            font-size:44px;
            font-weight:800;
            color:{text};
            min-width:100px;
            text-align:center;
        ">
            {final_score}
        </div>

        <div>
            <div style="
                font-size:1.15rem;
                font-weight:700;
                color:{text};
                margin-bottom:6px;
            ">
                {label}
            </div>

            <div style="
                font-size:0.95rem;
                line-height:1.55;
                color:#333;
            ">
                Overall neighbourhood risk is assessed as
                <strong>{label.lower()}</strong>, based on a composite
                assessment of location, zoning, local government area
                and marketability indicators.
            </div>
        </div>
    </div>
    """,
    height=140,
)

# =====================================================
# Risk Component Breakdown
# =====================================================
st.subheader("🔍 Risk Component Breakdown")

html_rows = ""
manual_review_target = None   # 保存需要人工复核的 component

for name, comp in components_data.items():

    # -------------------------------------------------
    # Detect manual override
    # -------------------------------------------------
    is_manually_reviewed = name in applied_overrides

    # -------------------------------------------------
    # Apply manual override score if exists
    # -------------------------------------------------
    if is_manually_reviewed:
        score = applied_overrides[name]["adjusted_score"]
    else:
        score = comp.get("score")

    rationale = comp.get("rationale", "See detailed policy interpretation")

    # -------------------------------------------------
    # 🔑 Dynamic risk label derived from CURRENT score
    # -------------------------------------------------
    if score is None:
        label = "Unknown"
    elif score >= 70:
        label = "Low Risk"
    elif score >= 50:
        label = "Moderate Risk"
    else:
        label = "Elevated Risk"

    # -------------------------------------------------
    # Visual priority: Manual Reviewed > Policy Warning > Normal
    # -------------------------------------------------
    left_border = "none"
    row_bg_override = None
    badge_html = ""

    # 🟠 1. Manually Reviewed (highest priority)
    if is_manually_reviewed:
        row_bg_override = "#fff7ed"
        left_border = "6px solid #f59e0b"

        justification_note = html.escape(
            applied_overrides[name].get(
                "justification",
                "Manual override applied."
            )
        )

        badge_html = f"""
        <span
            title="{justification_note}"
            style="
                padding:2px 8px;
                border-radius:999px;
                font-size:0.7rem;
                font-weight:700;
                background:#fed7aa;
                color:#9a3412;
                cursor:help;
            "
        >
            ✏️ Manually Reviewed
        </span>
        """

    # 🔴 2. Policy Warning (only if NOT manually reviewed)
    elif name == "Zoning" and summary.get("zoning") == "R4":
        left_border = "6px solid #c62828"

        manual_review_target = {
            "module": "Neighbourhood",
            "component": "Zoning",
            "original_score": score,
            "trigger": "Policy Warning",
            "context": {
                "zoning": summary.get("zoning")
            },
            "policy": ZONING_POLICY_REGISTRY.get("R4")
        }

        badge_html = """
        <span style="
            padding:2px 6px;
            border-radius:999px;
            font-size:0.7rem;
            font-weight:700;
            background:#fde68a;
            color:#92400e;
        ">
            ⚠ Policy
        </span>
        """

    # -------------------------------------------------
    # Base styling by UPDATED risk label
    # -------------------------------------------------
    if label == "Low Risk":
        bg = "#f3faf6"
        pill_bg = "#e6f4ea"
        pill_text = "#1b5e20"
    elif label == "Moderate Risk":
        bg = "#fff8eb"
        pill_bg = "#fff1cc"
        pill_text = "#8d6e00"
    else:  # Elevated Risk
        bg = "#fdecea"
        pill_bg = "#f9d6d5"
        pill_text = "#8e0000"

    # Override background if manually reviewed
    if row_bg_override:
        bg = row_bg_override

    html_rows += f"""
    <div style="
        display:grid;
        grid-template-columns: 1.4fr 0.7fr 1fr 2.4fr;
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
            {score if score is not None else "—"}
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
            grid-template-columns: 1.4fr 0.7fr 1fr 2.4fr;
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
            <div>Risk Rating</div>
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
    st.subheader("📝 Manual Review & Override")

    st.info(
        "One or more risk components require manual review under internal policy. "
        "A manual override may be requested with appropriate justification."
    )

    if st.button("⚠️ Request Manual Override for Zoning", use_container_width=True):
        st.session_state["manual_override"] = manual_review_target
        st.switch_page("pages/5_Manual_Review.py")

# =====================================================
# Navigation
# =====================================================
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Back to Neighbourhood Assessment", use_container_width=True):
        st.switch_page("pages/2_Neighbourhood_Risk.py")

with col2:
    if st.button("➡️ Continue to Land Risk Assessment", use_container_width=True):
        st.switch_page("pages/4_Land_Risk.py")

# =====================================================
# Disclaimer
# =====================================================
st.markdown("---")
st.caption("Decision-support tool only. Not a substitute for formal credit assessment.")