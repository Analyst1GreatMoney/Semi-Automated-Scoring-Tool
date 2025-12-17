def risk_label_to_score(label: str) -> int:
    """
    Convert qualitative risk label to numeric score (V1)
    """
    mapping = {
        "Low Risk": 80,
        "Moderate Risk": 60,
        "Elevated Risk": 30
    }
    return mapping.get(label, 50)
