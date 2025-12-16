import pandas as pd

def load_marketability_benchmarks_v1():
    """
    Marketability Benchmark Scoring Table

    Purpose:
        Quantify asset marketability for valuation and risk assessment.

    Version:
        1.0

    Interpretation:
        Higher score indicates better marketability and higher liquidity.
    """
    return pd.DataFrame({
        "level": [
            "Very Good",
            "Good",
            "Average",
            "Fair",
            "Poor"
        ],
        "meaning": [
            "High demand",
            "Normal demand",
            "Slow resale",
            "Hard to sell",
            "Very low liquidity"
        ],
        "marketability_score": [
            100,
            80,
            60,
            40,
            20
        ]
    })
