import pandas as pd

# =====================================================
# Benchmarks
# =====================================================

def load_marketability_benchmarks_v1():
    """
    Marketability Benchmark Scoring Table

    Version: 1.0
    Higher score = better liquidity / lower risk
    """
    return pd.DataFrame({
        "LEVEL": [
            "VERY GOOD",
            "GOOD",
            "AVERAGE",
            "FAIR",
            "POOR"
        ],
        "SCORE": [
            100,
            80,
            60,
            40,
            20
        ]
    })


# Load benchmark table once
MARKETABILITY_TABLE = load_marketability_benchmarks_v1()


# =====================================================
# Public Policy Interface
# =====================================================

def assess_marketability_risk(marketability_value: str) -> dict:
    """
    Policy entry point for Marketability risk assessment.

    Parameters
    ----------
    marketability_value : str
        One of: VERY GOOD, GOOD, AVERAGE, FAIR, POOR

    Returns
    -------
    dict
        Standardised risk result dictionary
    """

    if not marketability_value:
        return {
            "risk_name": "Marketability",
            "score": None,
            "label": "Unknown",
            "icon": "⚪",
            "flags": ["MISSING_MARKETABILITY"],
            "requires_manual_review": True,
        }

    marketability_value = marketability_value.upper().strip()

    row = MARKETABILITY_TABLE[
        MARKETABILITY_TABLE["LEVEL"] == marketability_value
    ]

    if row.empty:
        return {
            "risk_name": "Marketability",
            "score": None,
            "label": "Unknown",
            "icon": "⚪",
            "flags": ["INVALID_MARKETABILITY_VALUE"],
            "requires_manual_review": True,
        }

    score = int(row.iloc[0]["SCORE"])

    if score >= 80:
        label, icon = "Low Risk", "🟢"
    elif score >= 60:
        label, icon = "Moderate Risk", "🟡"
    else:
        label, icon = "Elevated Risk", "🔴"

    return {
        "risk_name": "Marketability",
        "score": score,
        "label": label,
        "icon": icon,
        "flags": [],
        "requires_manual_review": False,
    }
