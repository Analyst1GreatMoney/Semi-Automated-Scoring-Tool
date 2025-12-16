"""
Land Risk – Planning & Legal
Overlays Scoring Module

Source: Valuation Report (Overlay disclosures)
Version: 1.0
Purpose:
    - Interpret overlay-related wording from valuation reports
    - Classify overlay risk level
    - Assign numeric overlay score for land risk assessment
"""

# =========================================================
# 1. Overlay Keyword Benchmarks
#    (Derived from valuation report wording patterns)
# =========================================================

OVERLAY_KEYWORDS = {
    "very_high": [
        "unknown",
        "no formal searches undertaken",
        "overlay status not confirmed",
        "has not been investigated",
        "no planning certificate obtained",
        "further investigation required"
    ],
    "high": [
        "heritage overlay applies",
        "heritage listed",
        "environmental protection overlay applies",
        "environmental overlay affects the site",
        "overlays may materially restrict development",
        "significant planning limitation",
        "additional approvals required due to overlays"
    ],
    "medium": [
        "flood overlay applies",
        "flood-prone land",
        "subject to flood controls",
        "bushfire overlay applies",
        "bushfire prone land",
        "bal requirements apply",
        "overlays apply but are not considered onerous",
        "overlay requirements are manageable",
        "overlays are common to the locality"
    ],
    "low": [
        "no overlays affect the subject property",
        "no known planning overlays apply",
        "no adverse overlays identified",
        "no material overlays impacting use or development"
    ]
}

# =========================================================
# 2. Overlay Risk Level → Score Mapping
# =========================================================

OVERLAY_SCORE_MAP = {
    "low": 100,
    "medium": 70,
    "high": 40,
    "very_high": 20,
    "unknown": 50   # neutral fallback
}

# =========================================================
# 3. Core Classification Function
# =========================================================

def classify_overlay_effect(overlay_text: str) -> str:
    """
    Classify overlay effect based on wording from valuation report.

    Parameters
    ----------
    overlay_text : str
        Overlay-related description extracted from valuation report.

    Returns
    -------
    str
        Overlay risk level:
        'low', 'medium', 'high', 'very_high', or 'unknown'
    """

    if not isinstance(overlay_text, str):
        return "unknown"

    text = overlay_text.lower().strip()

    # Conservative risk-first principle
    for level in ["very_high", "high", "medium", "low"]:
        for keyword in OVERLAY_KEYWORDS[level]:
            if keyword in text:
                return level

    return "unknown"

# =========================================================
# 4. Overlay Effect Scoring Wrapper (Recommended Entry Point)
# =========================================================

def score_overlay_effect(overlay_text: str) -> dict:
    """
    Score overlay effect and return structured result.

    Parameters
    ----------
    overlay_text : str

    Returns
    -------
    dict
        {
            "overlay_risk_level": str,
            "overlay_score": int
        }
    """

    risk_level = classify_overlay_effect(overlay_text)
    score = OVERLAY_SCORE_MAP.get(risk_level, OVERLAY_SCORE_MAP["unknown"])

    return {
        "overlay_risk_level": risk_level,
        "overlay_score": score
    }

# =========================================================
# 5. Example Usage (for testing / debugging)
# =========================================================

if __name__ == "__main__":
    examples = [
        "No overlays affect the subject property",
        "Flood overlay applies, subject to standard controls",
        "Heritage overlay applies",
        "Unknown, no formal searches undertaken",
        "Overlay status has not been investigated"
    ]

    for text in examples:
        print(text, "->", score_overlay_effect(text))
