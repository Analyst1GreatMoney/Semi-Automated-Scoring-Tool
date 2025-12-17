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
