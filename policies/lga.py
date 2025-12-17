import pandas as pd

from data.normalisation import normalise_lga_name
from data.location import get_location_datasets


# =====================================================
# Load data (policy-owned, read-only)
# =====================================================
_datasets = get_location_datasets()
lga_irsad_df = _datasets.get("lga_irsad", pd.DataFrame())


# =====================================================
# Policy: LGA Risk
# =====================================================
def assess_lga_risk(lga_name: str) -> dict:
    """
    Assess LGA-level socio-economic risk using IRSAD decile.

    Parameters
    ----------
    lga_name : str
        Raw LGA name input by user.

    Returns
    -------
    dict
        Standardised risk result dictionary.
    """

    if not lga_name:
        return {
            "risk_name": "LGA Socio-Economic",
            "score": None,
            "label": "Unknown",
            "icon": "⚪",
            "flags": ["MISSING_LGA"],
            "requires_manual_review": True,
        }

    lga_key = normalise_lga_name(lga_name)

    # -------------------------------------------------
    # Defensive: dataset not available
    # -------------------------------------------------
    if lga_irsad_df.empty or "LGA_KEY" not in lga_irsad_df.columns:
        return {
            "risk_name": "LGA Socio-Economic",
            "score": None,
            "label": "Unknown",
            "icon": "⚪",
            "flags": ["LGA_DATA_NOT_AVAILABLE"],
            "requires_manual_review": True,
        }

    match = lga_irsad_df[lga_irsad_df["LGA_KEY"] == lga_key]

    if match.empty:
        return {
            "risk_name": "LGA Socio-Economic",
            "score": None,
            "label": "Unknown",
            "icon": "⚪",
            "flags": ["LGA_NOT_FOUND"],
            "requires_manual_review": True,
        }

    irsad_decile = int(match.iloc[0]["IRSAD_decile"])

    # -------------------------------------------------
    # IRSAD interpretation
    # -------------------------------------------------
    if irsad_decile >= 8:
        label, icon, score = "Low Risk", "🟢", 90
    elif irsad_decile >= 5:
        label, icon, score = "Moderate Risk", "🟡", 60
    else:
        label, icon, score = "Elevated Risk", "🔴", 30

    return {
        "risk_name": "LGA Socio-Economic",
        "score": score,
        "label": label,
        "icon": icon,
        "flags": [],
        "requires_manual_review": False,
    }
