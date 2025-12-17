import pandas as pd

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
# Classification Logic
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
# Policy Entry Point
# -------------------------------------------------
def assess_zoning_risk(zoning_code: str) -> dict:
    """
    Policy entry point for Zoning risk assessment.

    Parameters
    ----------
    zoning_code : str
        Planning zoning code (e.g. R2, R4, B4).

    Returns
    -------
    dict
        Standardised zoning risk result:
        - risk_name
        - score
        - label
        - icon
        - flags
        - requires_manual_review
    """

    # -----------------------------
    # Defensive handling
    # -----------------------------
    if not zoning_code:
        return {
            "risk_name": "Zoning",
            "score": 50,
            "label": "Unknown",
            "icon": "⚪",
            "flags": ["ZONING_MISSING"],
            "requires_manual_review": True,
        }

    zoning_code = zoning_code.upper().strip()

    res_df = load_residential_zoning_scoring_table()
    non_res_df = load_non_residential_zoning_scoring_table()

    flags: list[str] = []

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

        # Policy flags
        if zoning_code == "R4":
            flags.append("HIGH_DENSITY_RESIDENTIAL")

        return {
            "risk_name": "Zoning",
            "score": score,
            "label": label,
            "icon": icon,
            "flags": flags,
            "requires_manual_review": False,  # evaluated later by rules layer
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

        flags.append("NON_RESIDENTIAL_ZONING")

        if score <= 20:
            flags.append("RESTRICTIVE_ZONING")

        return {
            "risk_name": "Zoning",
            "score": score,
            "label": label,
            "icon": icon,
            "flags": flags,
            "requires_manual_review": False,
        }

    # -----------------------------
    # Unclassified zoning
    # -----------------------------
    return {
        "risk_name": "Zoning",
        "score": 20,
        "label": "High Risk",
        "icon": "🔴",
        "flags": ["UNCLASSIFIED_ZONING"],
        "requires_manual_review": True,
    }
