def build_location_narrative(
    crime_percentile,
    irsd_decile,
    irsad_decile,
    final_score,
    final_label,
) -> str:

    lines = []

    if crime_percentile is not None:
        lines.append(
            f"<strong>Crime:</strong> p{crime_percentile:.0f} "
            f"({'low risk' if crime_percentile >= 75 else 'average risk' if crime_percentile >= 50 else 'elevated risk'})"
        )

    if irsd_decile is not None:
        lines.append(
            f"<strong>IRSD:</strong> decile {irsd_decile} "
            f"({'low disadvantage' if irsd_decile >= 8 else 'moderate disadvantage' if irsd_decile >= 4 else 'high disadvantage'})"
        )

    if irsad_decile is not None:
        lines.append(
            f"<strong>IRSAD:</strong> decile {irsad_decile} "
            f"({'above-average profile' if irsad_decile >= 8 else 'mixed profile' if irsad_decile >= 4 else 'below-average profile'})"
        )

    lines.append(
        f"<strong>Overall:</strong> location risk assessed as <strong>{final_label.lower()}</strong>"
    )

    return "<br>".join(lines)
