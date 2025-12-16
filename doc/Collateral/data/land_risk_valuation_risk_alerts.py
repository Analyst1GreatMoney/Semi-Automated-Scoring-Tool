"""
Land Risk – Planning & Legal
Valuation Risk Alerts Scoring Module

Source: Valuation Report (Valuation Risk Alerts)
Version: 1.0
Purpose:
    - Interpret valuer-flagged critical risk alerts
    - Assign binary land risk outcome and numeric score
"""

# =========================================================
# 1. Valuation Risk Alert Benchmark
# =========================================================

VALUATION_RISK_ALERT_SCORE_MAP = {
    "no": {
        "risk_level": "low",
        "score": 100
    },
    "yes": {
        "risk_level": "very_high",
        "score": 20
    }
}

# =========================================================
# 2. Core Classification Function
# =========================================================

def classify_valuation_risk_alert(response: str) -> str:
    """
    Classify valuation risk alert response.

    Parameters
    ----------
    response : str
        Valuation Risk Alert response (expected: 'Yes' or 'No').

    Returns
    -------
    str
        Risk level: 'low', 'very_high', or 'unknown'
    """

    if not isinstance(response, str):
        return "unknown"

    text = response.strip().lower()

    if text == "yes":
        return "very_high"
    elif text == "no":
        return "low"
    else:
        return "unknown"

# =========================================================
# 3. Valuation Risk Alert Scoring Wrapper
# =========================================================

def score_valuation_risk_alert(response: str) -> dict:
    """
    Score valuation risk alert and return structured result.

    Parameters
    ----------
    response : str
        Valuation Risk Alert response ('Yes' / 'No').

    Returns
    -------
    dict
        {
            "valuation_risk_level": str,
            "valuation_risk_score": int
        }
    """

    if not isinstance(response, str):
        return {
            "valuation_risk_level": "unknown",
            "valuation_risk_score": 50
        }

    key = response.strip().lower()

    if key in VALUATION_RISK_ALERT_SCORE_MAP:
        result = VALUATION_RISK_ALERT_SCORE_MAP[key]
        return {
            "valuation_risk_level": result["risk_level"],
            "valuation_risk_score": result["score"]
        }

    # Fallback for unexpected values
    return {
        "valuation_risk_level": "unknown",
        "valuation_risk_score": 50
    }

# =========================================================
# 4. Example Usage (for testing / debugging)
# =========================================================

if __name__ == "__main__":
    examples = ["Yes", "No", "YES", "no", None, "Unknown"]

    for e in examples:
        print(e, "->", score_valuation_risk_alert(e))
