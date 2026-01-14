import pandas as pd
from typing import Dict, List

# -------------------------------------------------
# Zoning Scoring Tables
# -------------------------------------------------
def load_residential_zoning_scoring_table() -> pd.DataFrame:
    """
    Residential zoning scoring table.
    Higher score = better collateral liquidity.
    """
    return pd.DataFrame({
        "Zoning Code": ["R1", "R2", "R3", "R4", "R5"],
        "Score": [65, 80, 55, 30, 50]
    })


def load_non_residential_zoning_scoring_table() -> pd.DataFrame:
    """
    Non-residential and special-use zoning scoring table.
    """
    return pd.DataFrame({
        "Zoning Code": [
            "RU1","RU2","RU3","RU4","RU5","RU6",
            "B1","B2","B3","B4","B5","B6","B7","B8",
            "IN1","IN2","IN3","IN4",
            "SP1","SP2","SP3",
            "RE1","RE2",
            "E1","E2","E3","E4",
            "W1","W2","W3"
        ],
        "Score": [
            10,15,5,20,60,25,
            40,35,15,30,10,10,5,20,
            5,10,0,0,
            5,0,20,
            5,15,
            0,5,15,45,
            0,5,0
        ]
    })


# -------------------------------------------------
# Risk Classification Logic
# -------------------------------------------------
def classify_zoning_risk(score: int) -> tuple[str, str]:
    """
    Classify zoning risk based on numeric score.
    Returns (risk_label, icon).
    """
    if score >= 70:
        return "Low Risk", "🟢"
    elif score >= 50:
        return "Moderate Risk", "🟡"
    else:
        return "Elevated Risk", "🔴"


# -------------------------------------------------
# Zoning Policy Registry (Semantic Layer)
# -------------------------------------------------
ZONING_POLICY_REGISTRY: Dict[str, Dict] = {
    "R4": {
        "title": "R4 – High Density Residential",
        "policy_basis": [
            "Higher development intensity",
            "Increased planning and approval complexity",
            "Greater variability in resale and exit conditions",
        ],
        "requires_manual_review": True,
        "severity": "Elevated",
        "flag": "HIGH_DENSITY_RESIDENTIAL",
    },
    "NON_RESIDENTIAL": {
        "title": "Non-Residential Zoning",
        "policy_basis": [
            "Zoning not primarily intended for residential use",
            "Potential limitations on owner-occupier demand",
            "Higher exit and liquidity uncertainty",
        ],
        "requires_manual_review": True,
        "severity": "Elevated",
        "flag": "NON_RESIDENTIAL_ZONING",
    },
    "UNCLASSIFIED": {
        "title": "Unclassified Zoning",
        "policy_basis": [
            "Zoning code not recognised by internal classification",
            "Increased uncertainty in planning permissibility",
        ],
        "requires_manual_review": True,
        "severity": "High",
        "flag": "UNCLASSIFIED_ZONING",
    },
}


# -------------------------------------------------
# Policy Entry Point
# -------------------------------------------------
def assess_zoning_risk(zoning_code: str) -> dict:
    """
    Policy entry point for Zoning risk assessment.

    Returns a standardised zoning risk object that supports:
    - scoring
    - policy flags
    - manual review
    - UI policy rendering
    """

    # -----------------------------
    # Defensive handling
    # -----------------------------
    if not zoning_code:
        return {
            "risk_name": "Zoning",
            "zoning_code": None,
            "score": 50,
            "label": "Unknown",
            "icon": "⚪",
            "flags": ["ZONING_MISSING"],
            "requires_manual_review": True,
            "policy": None,
        }

    zoning_code = zoning_code.upper().strip()

    res_df = load_residential_zoning_scoring_table()
    non_res_df = load_non_residential_zoning_scoring_table()

    flags: List[str] = []
    policy_context = None

    # -----------------------------
    # Residential zoning
    # -----------------------------
    if zoning_code in res_df["Zoning Code"].values:
        score = int(
            res_df.loc[
                res_df["Zoning Code"] == zoning_code, "Score"
            ].values[0]
        )

        label, icon = classify_zoning_risk(score)

        if zoning_code in ZONING_POLICY_REGISTRY:
            policy_context = ZONING_POLICY_REGISTRY[zoning_code]
            flags.append(policy_context["flag"])

        return {
            "risk_name": "Zoning",
            "zoning_code": zoning_code,
            "score": score,
            "label": label,
            "icon": icon,
            "flags": flags,
            "requires_manual_review": policy_context["requires_manual_review"]
            if policy_context else False,
            "policy": policy_context,
        }

    # -----------------------------
    # Non-residential / special zoning
    # -----------------------------
    if zoning_code in non_res_df["Zoning Code"].values:
        score = int(
            non_res_df.loc[
                non_res_df["Zoning Code"] == zoning_code, "Score"
            ].values[0]
        )

        label, icon = classify_zoning_risk(score)

        policy_context = ZONING_POLICY_REGISTRY["NON_RESIDENTIAL"]
        flags.append(policy_context["flag"])

        if score <= 20:
            flags.append("RESTRICTIVE_ZONING")

        return {
            "risk_name": "Zoning",
            "zoning_code": zoning_code,
            "score": score,
            "label": label,
            "icon": icon,
            "flags": flags,
            "requires_manual_review": policy_context["requires_manual_review"],
            "policy": policy_context,
        }

    # -----------------------------
    # Unclassified zoning
    # -----------------------------
    policy_context = ZONING_POLICY_REGISTRY["UNCLASSIFIED"]

    return {
        "risk_name": "Zoning",
        "zoning_code": zoning_code,
        "score": 20,
        "label": "Elevated Risk",
        "icon": "🔴",
        "flags": [policy_context["flag"]],
        "requires_manual_review": policy_context["requires_manual_review"],
        "policy": policy_context,
    }