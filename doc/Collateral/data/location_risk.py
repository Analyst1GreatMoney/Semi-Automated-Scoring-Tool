def calculate_property_address_score_v1(
    irsd_score: float,
    irsad_score: float,
    crime_score: float
):
    """
    Calculate Property Address Raw Score (Version 1.0)

    Weighting:
    - Suburb socio-economic level (IRSD + IRSAD): 50%
    - Suburb crime level: 50%

    Parameters
    ----------
    irsd_score : float
        IRSD score (10–100)
    irsad_score : float
        IRSAD score (10–100)
    crime_score : float
        Crime risk score (0–100, higher = safer)

    Returns
    -------
    dict
        {
            "socio_economic_score": float,
            "address_raw_score": float
        }
    """

    # 1️⃣ Socio-economic composite
    socio_economic_score = (irsd_score + irsad_score) / 2

    # 2️⃣ Address raw score (50 / 50 weighting)
    address_raw_score = (
        0.5 * socio_economic_score +
        0.5 * crime_score
    )

    return {
        "socio_economic_score": round(socio_economic_score, 2),
        "address_raw_score": round(address_raw_score, 2)
    }
