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

def resolve_marketability_risk(marketability_value: str):
    """
    Resolve marketability risk based on benchmark score
    """

    row = marketability_table[
        marketability_table["LEVEL"] == marketability_value
    ]

    if row.empty:
        return "Unknown", "⚪", "Marketability information not available."

    score = int(row.iloc[0]["SCORE"])

    if score >= 80:
        return (
            "Low Risk",
            "🟢",
            "Strong resale demand and high market liquidity."
        )
    elif score >= 60:
        return (
            "Moderate Risk",
            "🟡",
            "Average liquidity with potential for slower resale."
        )
    else:
        return (
            "Elevated Risk",
            "🔴",
            "Limited buyer demand and reduced resale liquidity."
        )
