# =====================================================
# Policy Layer – Location Scoring
# =====================================================
def load_irsd_scoring_table():
    return pd.DataFrame({
        "IRSD_Decile": range(1, 11),
        "Score": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    })


def load_irsad_scoring_table():
    return pd.DataFrame({
        "IRSAD_Decile": range(1, 11),
        "Score": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    })


def crime_score_from_percentile(percentile: float) -> int:
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


def calculate_location_risk_score(crime_score, irsd_score, irsad_score):
    return round(
        0.4 * crime_score +
        0.3 * irsd_score +
        0.3 * irsad_score,
        1
    )


def classify_location_risk(score):
    if score >= 75:
        return "Low Risk", "🟢"
    elif score >= 50:
        return "Moderate Risk", "🟡"
    else:
        return "Elevated Risk", "🔴"

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

def assess_location_risk(
    crime_percentile: float,
    irsd_decile: int,
    irsad_decile: int,
) -> dict:
    """
    Policy entry point for Location / Neighbourhood risk assessment.

    This function orchestrates suburb-level crime risk and socio-economic
    indicators (IRSD, IRSAD) to produce a composite location / neighbourhood
    risk score and classification.

    Parameters
    ----------
    crime_percentile : float
        Crime percentile ranking for the suburb (0–100).
    irsd_decile : int
        IRSD decile (1–10), where 10 indicates least disadvantage.
    irsad_decile : int
        IRSAD decile (1–10), where 10 indicates greatest advantage.

    Returns
    -------
    dict
        Standardised risk result dictionary containing:
        - risk_name
        - score
        - label
        - icon
        - flags
        - requires_manual_review
    """

    # -----------------------------
    # Step 1: Convert raw inputs to scores
    # -----------------------------
    crime_score = crime_score_from_percentile(crime_percentile)

    irsd_score = load_irsd_scoring_table().loc[
        lambda df: df["IRSD_Decile"] == irsd_decile, "Score"
    ].values[0]

    irsad_score = load_irsad_scoring_table().loc[
        lambda df: df["IRSAD_Decile"] == irsad_decile, "Score"
    ].values[0]

    # -----------------------------
    # Step 2: Calculate composite numeric score
    # -----------------------------
    score = calculate_location_risk_score(
        crime_score=crime_score,
        irsd_score=irsd_score,
        irsad_score=irsad_score,
    )

    # -----------------------------
    # Step 3: Classify risk outcome
    # -----------------------------
    label, icon = classify_composite_location_risk(score)

    # -----------------------------
    # Step 4: Return standardised result
    # -----------------------------
    return {
        "risk_name": "Location / Neighbourhood",
        "score": score,
        "label": label,
        "icon": icon,
        "flags": [],  # populated later by rules/flags.py
        "requires_manual_review": False,  # evaluated later by rules/manual_review.py
    }
