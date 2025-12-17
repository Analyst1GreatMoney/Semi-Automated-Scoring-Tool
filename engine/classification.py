# =====================================================
# Composite Location Risk Classification
# =====================================================

def classify_composite_location_risk(score: int):
    """
    Classify composite location risk score.

    Parameters
    ----------
    score : int
        Composite location / neighbourhood score (0–100)

    Returns
    -------
    tuple[str, str]
        (final_label, final_icon)
    """

    if score >= 80:
        return "Low Risk", "🟢"
    elif score >= 60:
        return "Moderate Risk", "🟡"
    else:
        return "Elevated Risk", "🔴"
