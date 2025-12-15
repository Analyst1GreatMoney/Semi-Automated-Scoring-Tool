import pandas as pd

def load_residential_zoning_scoring_table():
    """
    Residential Zoning Scoring Table
    Source: NSW Standard Instrument LEP
    Scope: Residential Zones Only (R1–R5)
    Version: 1.0
    """

    return pd.DataFrame({
        "Zoning Code": ["R1", "R2", "R3", "R4", "R5"],
        "Zoning Name": [
            "General Residential",
            "Low Density Residential",
            "Medium Density Residential",
            "High Density Residential",
            "Large Lot Residential"
        ],
        "Description": [
            "Broad range of residential densities and housing types, including multi-dwelling and residential flat buildings, with supporting community uses.",
            "Primarily low density housing with detached dwellings; most restrictive urban residential zone.",
            "Medium density accommodation allowing housing diversity and moderate redevelopment potential.",
            "Primarily high density housing such as apartments with supporting residential services.",
            "Residential housing in a rural or semi-rural setting, often adjacent to towns or metropolitan areas."
        ],
        "Score (V1.0)": [65, 80, 55, 30, 50]
    })
