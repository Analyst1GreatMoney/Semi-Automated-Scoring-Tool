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

def assess_marketability_risk(marketability: str) -> dict:
    mapping = {
        "VERY GOOD": (90, "Low Risk"),
        "GOOD": (80, "Low Risk"),
        "AVERAGE": (60, "Moderate Risk"),
        "FAIR": (40, "Elevated Risk"),
        "POOR": (20, "High Risk"),
    }

    if not marketability:
        return {
            "score": None,
            "label": "Unknown",
            "rationale": "Marketability assessment not provided."
        }

    marketability = marketability.upper().strip()

    score, label = mapping.get(
        marketability,
        (None, "Unknown")
    )

    return {
        "score": score,
        "label": label,
        "rationale": "See detailed policy interpretation"
    }

