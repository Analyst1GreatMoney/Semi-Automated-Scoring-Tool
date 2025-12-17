from typing import List, Dict


def compute_location_neighbourhood_score(
    results: List[Dict],
    weights: Dict[str, float] | None = None,
    debug: bool = False,   # 👈 ① 加在这里
) -> float | Dict:
    """
    Compute composite Location / Neighbourhood risk score.
    """

    if not results:
        raise ValueError("No risk results provided.")

    # -----------------------------
    # Validate results structure
    # -----------------------------
    valid_results = []
    for r in results:
        if "risk_name" not in r or "score" not in r:
            continue
        if r["score"] is None:
            continue
        valid_results.append(r)

    if not valid_results:
        raise ValueError("No valid risk scores found.")

    # -----------------------------
    # Default equal weights
    # -----------------------------
    if weights is None:
        equal_weight = 1 / len(valid_results)
        weights = {
            r["risk_name"]: equal_weight
            for r in valid_results
        }

    # -----------------------------
    # Weighted aggregation
    # -----------------------------
    total_score = 0.0
    total_weight = 0.0

    for r in valid_results:
        name = r["risk_name"]
        score = r["score"]

        w = weights.get(name, 0)

        if w <= 0:
            continue

        total_score += score * w
        total_weight += w

    if total_weight == 0:
        raise ValueError("Total weight is zero. Check weight configuration.")

    final_score = round(total_score / total_weight, 1)

    # -----------------------------
    # Debug output
    # -----------------------------
    if debug:   # 👈 ② 加在 return 前
        return {
            "inputs": valid_results,
            "weights": weights,
            "total_weight": total_weight,
            "raw_score": total_score,
            "score": final_score,
        }

    return final_score  # 👈 ③ 原 return 留在这里
