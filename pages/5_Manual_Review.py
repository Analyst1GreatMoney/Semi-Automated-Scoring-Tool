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
    page_title="Manual Review & Override",
    page_icon="📝",
    layout="centered",
)

# =====================================================
# Load Manual Override Context
# =====================================================
override_ctx = st.session_state.get("manual_override")

if not override_ctx:
    st.error(
        "No manual review context found. "
        "Please return to the previous assessment page and request a manual override again."
    )
    st.stop()

# -----------------------------
# Unpack context safely
# -----------------------------
module = override_ctx.get("module", "Unknown")
component = override_ctx.get("component", "Unknown")
original_score = override_ctx.get("original_score", 50)
trigger = override_ctx.get("trigger", "Policy Warning")
context = override_ctx.get("context", {})
policy = override_ctx.get("policy")

# =====================================================
# Defensive Policy Fallback (CRITICAL)
# =====================================================
if not policy:
    policy = {
        "title": "Policy Review Required",
        "policy_basis": [
            "This risk component has triggered a manual review under internal policy.",
            "No detailed policy rule was supplied by the upstream assessment.",
            "Professional judgement is required to determine risk acceptability."
        ]
    }

policy_title = policy.get("title", "Policy Review Required")
policy_basis = policy.get("policy_basis", [])

# =====================================================
# Header
# =====================================================
st.title("📝 Manual Review & Override")
st.caption("Human-in-the-loop • Policy Exception Review")

st.info(
    "This risk component has been flagged for manual review under internal policy. "
    "A manual override may be applied with appropriate professional justification."
)

st.markdown("---")

# =====================================================
# Review Context + Policy (Merged, Exact Breakdown UI)
# =====================================================
st.subheader("📌 Review Context")

# -----------------------------
# Risk styling (same logic as breakdown)
# -----------------------------
if original_score >= 70:
    risk_label = "Low Risk"
    bg = "#f3faf6"
    pill_bg = "#e6f4ea"
    pill_text = "#1b5e20"
elif original_score >= 50:
    risk_label = "Moderate Risk"
    bg = "#fff8eb"
    pill_bg = "#fff1cc"
    pill_text = "#8d6e00"
else:
    risk_label = "Elevated Risk"
    bg = "#fdecea"
    pill_bg = "#f9d6d5"
    pill_text = "#8e0000"

components.html(
    f"""
    <div style="
        margin-top:12px;
        padding:16px;
        border-radius:14px;
        background:#ffffff;
        border:1px solid #e5e7eb;
    ">

        <!-- Risk Component Row (EXACT SAME AS BREAKDOWN) -->
        <div style="
            display:grid;
            grid-template-columns: 1.4fr 0.7fr 1fr 2.4fr;
            column-gap:16px;
            padding:14px 16px;
            margin-bottom:12px;
            border-radius:10px;
            background:{bg};
            align-items:start;
        ">
            <div style="font-weight:600;">{component}</div>

            <div style="font-weight:600;">
                {original_score}
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
                    {risk_label}
                </span>
            </div>

            <div style="font-size:0.85rem; line-height:1.6; color:#333;">
                {policy_title}
                <span style="color:#d97706;">⚠️</span>
            </div>
        </div>

        <!-- Policy Basis -->
        <div style="
            padding:4px 16px 10px 16px;
            font-size:0.85rem;
            line-height:1.6;
            color:#444;
        ">
            <div style="font-weight:600; margin-bottom:6px;">
                📄 Policy Basis
            </div>

            <ul style="margin:0 0 8px 18px; padding:0;">
                {''.join(f"<li>{item}</li>" for item in policy_basis)}
            </ul>

            <div style="color:#666;">
                Manual assessment is required before any score override is applied.
            </div>
        </div>

    </div>
    """,
    height=260,
)

st.markdown("---")

# =====================================================
# Manual Score Adjustment
# =====================================================
st.subheader("✏️ Manual Score Adjustment")

new_score = st.slider(
    "Adjusted Score",
    min_value=0,
    max_value=100,
    value=int(original_score),
    help="Adjust the component score based on professional judgement."
)

justification = st.text_area(
    "Override Justification (Required)",
    placeholder=(
        "Provide a clear, concise justification for overriding the system-generated score. "
        "This justification is mandatory for audit and governance purposes."
    ),
    height=140,
)

# =====================================================
# Action Buttons
# =====================================================
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("❌ Cancel Override", use_container_width=True):
        st.switch_page("pages/3_Neighbourhood_Risk_Results.py")

with col2:
    if st.button("✅ Confirm Override", use_container_width=True):
        if not justification.strip():
            st.error("Override justification is required.")
        else:
            st.session_state["override_result"] = {
                "module": module,
                "component": component,
                "original_score": original_score,
                "adjusted_score": new_score,
                "justification": justification,
                "trigger": trigger,
                "policy": policy,
                "context": context,
            }

            st.success("Manual override has been recorded successfully.")
            st.switch_page("pages/3_Neighbourhood_Risk_Results.py")

# =====================================================
# Disclaimer
# =====================================================
st.markdown("---")
st.caption(
    "Manual overrides are logged for audit, governance, and model risk management purposes. "
    "All adjustments must comply with internal credit policy."
)