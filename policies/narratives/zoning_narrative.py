def build_zoning_narrative(
    zoning_code: str,
    label: str,
) -> str:
    """
    Lightweight zoning narrative for Results page.
    Mirrors Location narrative density.
    """

    lines: list[str] = []

    # -----------------------------
    # Zoning classification
    # -----------------------------
    if zoning_code:
        lines.append(
            f"<strong>Zoning:</strong> {zoning_code}"
        )
    else:
        lines.append(
            "<strong>Zoning:</strong> not specified"
        )

    # -----------------------------
    # Overall conclusion
    # -----------------------------
    lines.append(
        f"<strong>Overall:</strong> zoning risk assessed as "
        f"<strong>{label.lower()}</strong>"
    )

    return "<br>".join(lines)