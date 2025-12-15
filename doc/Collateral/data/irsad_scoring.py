import pandas as pd

def load_irsad_scoring_table():
    """
    IRSAD Decile Scoring Table
    Source: ABS SEIFA (IRSAD)
    Version: 1.0
    """
    return pd.DataFrame({
        "IRSAD Decile": range(1, 11),
        "Interpretation": [
            "Most disadvantaged",
            "Very disadvantaged",
            "Disadvantaged",
            "Below average",
            "Average",
            "Slightly advantaged",
            "Moderately advantaged",
            "Advantaged",
            "Very advantaged",
            "Most advantaged"
        ],
        "Score (V1.0)": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    })
