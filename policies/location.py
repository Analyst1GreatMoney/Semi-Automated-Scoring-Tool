import pandas as pd

# =====================================================
# Scoring Tables
# =====================================================
def load_irsd_scoring_table():
    return pd.DataFrame({
        "IRSD_Decile": range(1, 11),
        "Score": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    })


def load_irsad_scoring_table():
    return pd.DataFrame({
        "IRSAD_Decile": range(1, 11),
        "Score": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    })


# =====================================================
# Helper – Safe lookup
# =====================================================
def lookup_score(table: pd.DataFrame, key_col: str, key):
    """
    Safely look up a score from a scoring table.
    Returns None if key is missing or not found.
    """
    if key is None:
        return None

    match = table.loc[table[key_col] == key, "Score"]
    if match.empty:
        return None

    return int(match.values[0])


# =====================================================
# Crime Scoring
# =====================================================
def crime_score_from_percentile(percentile):
    """
    Convert crime percentile (0–100) to risk score.
    Higher score = lower risk.
    """
    if percentile is None:
        return None

    if percentile >= 90:
        return 100
    elif percentile >= 75:
        return 80
    elif percentile >= 50:
        return 60
    elif percentile >= 25:
        return 40
    else:
        return 20


# =====================================================
# Composite Calculation
# =====================================================
def calculate_location_risk_score(crime_score, irsd_score, irsad_score):
    return round(
        0.4 * crime_score +
        0.3 * irsd_score +
        0.3 * irsad_score,
        1
    )


def classify_composite_location_risk(score):
    """
    Composite Location / Neighbourhood Risk Classification
    Input: numeric score (0–100)
    Output: (risk_label, icon)
    """
    if score >= 75:
        return "Low Risk", "🟢"
    elif score >= 50:
        return "Moderate Risk", "🟡"
    else:
        return "Elevated Risk", "🔴"


# =====================================================
# Public Policy Entry Point
# =====================================================
def assess_location_risk(
    crime_percentile: float,
    irsd_decile: int,
    irsad_decile: int,
) -> dict:
    """
    Policy entry point for Location / Neighbourhood risk assessment.

    Accepts incomplete data (None) and degrades gracefully
    for semi-automated decision support.
    """

    # -----------------------------
    # Step 1: Convert raw inputs to scores
    # -----------------------------
    crime_score = crime_score_from_percentile(crime_percentile)

    irsd_score = lookup_score(
        load_irsd_scoring_table(),
        "IRSD_Decile",
        irsd_decile,
    )

    irsad_score = lookup_score(
        load_irsad_scoring_table(),
        "IRSAD_Decile",
        irsad_decile,
    )

    # -----------------------------
    # Step 2: Guard – incomplete data
    # -----------------------------
    if any(v is None for v in [crime_score, irsd_score, irsad_score]):
        return {
            "risk_name": "Location / Neighbourhood",
            "score": None,
            "label": "Unknown",
            "icon": "⚪",
            "flags": ["INCOMPLETE_DATA"],
            "requires_manual_review": True,
        }

    # -----------------------------
    # Step 3: Calculate composite score
    # -----------------------------
    score = calculate_location_risk_score(
        crime_score=crime_score,
        irsd_score=irsd_score,
        irsad_score=irsad_score,
    )

    # -----------------------------
    # Step 4: Classify risk outcome
    # -----------------------------
    label, icon = classify_composite_location_risk(score)

    # -----------------------------
    # Step 5: Return standardised result
    # -----------------------------
    return {
        "risk_name": "Location / Neighbourhood",
        "score": score,
        "label": label,
        "icon": icon,
        "flags": [],
        "requires_manual_review": False,
    }
