def resolve_lga_irsad_risk(lga_name: str):
    """
    Resolve LGA-level IRSAD risk from user input.
    Returns: (risk_label, icon, explanation)
    """

    if not lga_name:
        return "Unknown", "⚪", "Local Government Area not provided."

    lga_key = normalise_lga_name(lga_name)

    match = lga_irsad_df[lga_irsad_df["LGA_KEY"] == lga_key]

    if match.empty:
        return "Unknown", "⚪", "LGA not found in socio-economic database."

    irsad_decile = int(match.iloc[0]["IRSAD_decile"])

    # Reuse IRSAD decile logic (hidden from UI)
    if irsad_decile >= 8:
        return "Low Risk", "🟢", "LGA shows strong socio-economic advantage."
    elif irsad_decile >= 5:
        return "Moderate Risk", "🟡", "LGA shows average socio-economic conditions."
    else:
        return "Elevated Risk", "🔴", "LGA shows relative socio-economic disadvantage."
