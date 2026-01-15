def risk_label_to_score_legacy(label: str) -> int:
    """
    Legacy / fallback mapping.
    Use ONLY when numeric score is unavailable.
    """
    mapping = {
        "Low Risk": 80,
        "Moderate Risk": 60,
        "Elevated Risk": 30
    }
    return mapping.get(label, 50)

def score_to_risk_label(score: int) -> str:
    """
    Convert numeric score to qualitative risk label (UI logic)
    """
    if score >= 70:
        return "Low Risk"
    elif score >= 50:
        return "Moderate Risk"
    else:
        return "Elevated Risk"
