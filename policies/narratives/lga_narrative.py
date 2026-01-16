def build_lga_narrative(
    lga_name: str,
    label: str,
) -> str:
    """
    Lightweight LGA narrative for Results page.
    Mirrors Location and Zoning narrative density.
    """

    lines: list[str] = []

    # -----------------------------
    # LGA identification
    # -----------------------------
    if lga_name:
        lines.append(
            f"<strong>LGA:</strong> {lga_name}"
        )
    else:
        lines.append(
            "<strong>LGA:</strong> not specified"
        )

    # -----------------------------
    # Overall conclusion
    # -----------------------------
    lines.append(
        f"<strong>Overall:</strong> LGA risk assessed as "
        f"<strong>{label.lower()}</strong>"
    )

    return "<br>".join(lines)