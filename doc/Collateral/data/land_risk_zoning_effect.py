"""
Land Risk – Planning & Legal
Zoning Effect Scoring Module

Source: Valuation Report (Zoning wording)
Version: 1.0
Purpose:
    - Convert zoning wording into structured zoning risk level
    - Assign numeric zoning score for land risk assessment
"""

# =========================================================
# 1. Zoning Effect Keyword Benchmarks
#    (Derived from valuation report wording patterns)
# =========================================================

ZONING_KEYWORDS = {
    "very_high": [
        "use is not permitted",
        "use prohibited",
        "not permitted",
        "zoning prohibits",
        "does not comply with zoning",
        "does not comply"
    ],
    "high": [
        "non-conforming",
        "non conforming",
        "existing use rights",
        "legal non-conformity",
        "zoning may restrict development",
        "significantly limits development",
        "adversely affect use"
    ],
    "medium_high": [
        "development potential may be limited",
        "development may be constrained",
        "planning controls restrict development"
    ],
    "medium": [
        "permitted subject to approval",
        "subject to approval",
        "subject to council consent",
        "subject to development approval",
        "subject to planning consent",
        "zoning allows existing use only",
        "existing use only",
        "redevelopment discouraged"
    ],
    "low": [
        "permits single residential property",
        "residential use is permitted",
        "zoned for residential",
        "zoned for residential purposes",
        "use is permissible",
        "existing use is permitted",
        "consistent with zoning",
        "appropriate zoning"
    ]
}

# =========================================================
# 2. Zoning Risk Level → Score Mapping
# =========================================================

ZONING_SCORE_MAP = {
    "low": 100,
    "medium": 70,
    "medium_high": 50,
    "high": 40,
    "very_high": 20,
    "unknown": 50  # neutral fallback
}

# =========================================================
# 3. Core Classification Function
# =========================================================

def classify_zoning_effect(zoning_text: str) -> str:
    """
    Classify zoning effect based on wording from valuation report.

    Parameters
    ----------
    zoning_text : str
        Zoning description extracted from valuation report.

    Returns
    -------
    str
        Zoning risk level:
        'low', 'medium', 'medium_high', 'high', 'very_high', or 'unknown'
    """

    if not isinstance(zoning_text, str):
        return "unknown"

    text = zoning_text.lower().strip()

    # Risk-first principle:
    # Always check higher risk levels first
    for level in ["very_high", "high", "medium_high", "medium", "low"]:
        for keyword in ZONING_KEYWORDS[level]:
            if keyword in text:
                return level

    return "unknown"

# =========================================================
# 4. Zoning Effect Scoring Wrapper (Recommended Entry Point)
# =========================================================

def score_zoning_effect(zoning_text: str) -> dict:
    """
    Score zoning effect and return structured result.

    Parameters
    ----------
    zoning_text : str

    Returns
    -------
    dict
        {
            "zoning_risk_level": str,
            "zoning_score": int
        }
    """

    risk_level = classify_zoning_effect(zoning_text)
    score = ZONING_SCORE_MAP.get(risk_level, ZONING_SCORE_MAP["unknown"])

    return {
        "zoning_risk_level": risk_level,
        "zoning_score": score
    }

# =========================================================
# 5. Example Usage (for testing / debugging)
# =========================================================
if __name__ == "__main__":
    examples = [
        "Permits single residential property",
        "Residential use is permitted, however development may be limited",
        "Zoning allows existing use only",
        "Non-conforming but existing use",
        "Use is not permitted under zoning"
    ]

    for text in examples:
        print(text, "->", score_zoning_effect(text))
