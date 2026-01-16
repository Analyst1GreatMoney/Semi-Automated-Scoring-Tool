def build_marketability_narrative(
    marketability_label: str,
    label: str,
) -> str:
    """
    Lightweight Marketability narrative for Results page.
    Mirrors Zoning and LGA narrative density.
    """

    lines: list[str] = []

    # -----------------------------
    # Marketability classification
    # -----------------------------
    if marketability_label:
        lines.append(
            f"<strong>Marketability:</strong> {marketability_label}"
        )
    else:
        lines.append(
            "<strong>Marketability:</strong> not specified"
        )

    # -----------------------------
    # Overall conclusion
    # -----------------------------
    lines.append(
        f"<strong>Overall:</strong> marketability risk assessed as "
        f"<strong>{label.lower()}</strong>"
    )

    return "<br>".join(lines)
