# =====================================================
# Composite Location Risk Classification
# =====================================================

def classify_composite_location_risk(score: float):
    if score < 40:
        return "High Risk", "#E74C3C"   # red
    elif score < 70:
        return "Moderate Risk", "#F1C40F"  # amber
    else:
        return "Low Risk", "#2ECC71"    # green
