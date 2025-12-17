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
