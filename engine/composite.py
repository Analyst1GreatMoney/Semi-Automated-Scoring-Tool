from typing import List, Dict


def compute_location_neighbourhood_score(
    results: List[Dict],
    weights: Dict[str, float] | None = None,
) -> float:
    """
    Compute composite Location / Neighbourhood risk score.

    Parameters
    ----------
    results : list of dict
        List of standardised risk result dictionaries.
        Each dict must contain:
        - risk_name (str)
        - score (int or float)

    weights : dict, optional
        Mapping of risk_name -> weight.
        If not provided, equal weighting is applied.

    Returns
    -------
    float
        Composite score (0–100), rounded to 1 decimal place.
    """

    if not results:
        raise ValueError("No risk results provided.")

    # -----------------------------
    # Default equal weights
    # -----------------------------
    if weights is None:
        weight = 1 / len(results)
        weights = {r["risk_name"]: weight for r in results}

    # -----------------------------
    # Weighted aggregation
    # -----------------------------
    total_score = 0.0
    total_weight = 0.0

    for r in results:
        name = r["risk_name"]
        score = r.get("score")

        if score is None:
            continue

        w = weights.get(name, 0)

        total_score += score * w
        total_weight += w

    if total_weight == 0:
        raise ValueError("Total weight is zero. Check weight configuration.")

    return round(total_score / total_weight, 1)
