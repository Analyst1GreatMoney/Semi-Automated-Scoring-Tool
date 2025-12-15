import pandas as pd

def load_irsd_scoring_table():
    """
    IRSD Decile Scoring Table
    Source: ABS SEIFA (IRSD)
    Version: 1.0
    """
    return pd.DataFrame({
        "IRSD Decile": range(1, 11),
        "Interpretation": [
            "Most disadvantaged",
            "Very disadvantaged",
            "Disadvantaged",
            "Below average",
            "Average",
            "Slightly above average",
            "Above average",
            "Good socio-economic profile",
            "Very good",
            "Most advantaged"
        ],
        "Score (V1.0)": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    })
