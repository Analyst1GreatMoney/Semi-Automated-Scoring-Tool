# =====================================================
# Utility: Suburb Normalisation
# =====================================================
def normalise_suburb_name(name: str) -> str:
    if pd.isna(name):
        return ""
    return (
        name.upper()
        .replace("(NSW)", "")
        .replace("(VIC)", "")
        .replace("(QLD)", "")
        .replace("(WA)", "")
        .replace("(SA)", "")
        .replace("(TAS)", "")
        .replace("(ACT)", "")
        .replace("(NT)", "")
        .strip()
    )

def normalise_lga_name(name: str) -> str:
    """
    Normalise LGA names for robust matching between:
    - Valuation reports (e.g. 'The Hills Shire Council')
    - ABS / IRSAD datasets (e.g. 'The Hills Shire')

    Strategy:
    - Uppercase
    - Remove state suffixes
    - Remove common administrative words (COUNCIL, CITY OF)
    - Normalise whitespace
    """

    if not name:
        return ""

    cleaned = (
        name.upper()
        .replace("(NSW)", "")
        .replace("(VIC)", "")
        .replace("(QLD)", "")
        .replace("(WA)", "")
        .replace("(SA)", "")
        .replace("(TAS)", "")
        .replace("(ACT)", "")
        .replace("(NT)", "")
        .replace("COUNCIL", "")
        .replace("CITY OF", "")
        .replace("CITY", "")   # optional but practical
        .strip()
    )

    # Collapse multiple spaces into one
    cleaned = " ".join(cleaned.split())

    return cleaned


