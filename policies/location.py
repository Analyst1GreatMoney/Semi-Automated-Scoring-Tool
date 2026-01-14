import pandas as pd
from typing import Optional, Dict


# =====================================================
# Scoring tables
# =====================================================
def _load_decile_scoring_table(decile_col: str) -> pd.DataFrame:
    return pd.DataFrame({
        decile_col: range(1, 11),
        "score": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    })


def _lookup_score(
    table: pd.DataFrame,
    key_col: str,
    key: Optional[int],
) -> Optional[int]:
    if key is None:
        return None

    match = table.loc[table[key_col] == key, "score"]
    if match.empty:
        return None

    return int(match.iloc[0])


# =====================================================
# Crime scoring
# =====================================================
def crime_score_from_percentile(percentile: Optional[float]) -> Optional[int]:
    """
    Higher score = lower risk
    """
    if percentile is None:
        return None

    if percentile >= 90:
        return 100
    elif percentile >= 75:
        return 80
    elif percentile >= 50:
        return 60
    elif percentile >= 25:
        return 40
    else:
        return 20


def crime_rationale(percentile: Optional[float]) -> str:
    if percentile is None:
        return "Crime data unavailable at suburb level."

    if percentile >= 75:
        return "Crime incidence is materially lower than comparable suburbs."
    elif percentile >= 50:
        return "Crime levels are broadly in line with metropolitan averages."
    else:
        return "Elevated crime incidence relative to comparable suburbs."


# =====================================================
# Composite calculation
# =====================================================
def calculate_location_score(
    crime_score: Optional[int],
    irsd_score: Optional[int],
    irsad_score: Optional[int],
) -> Optional[float]:
    """
    Weighted composite score.
    Automatically re-normalises weights if partial data.
    """

    components = {
        "crime": (crime_score, 0.4),
        "irsd": (irsd_score, 0.3),
        "irsad": (irsad_score, 0.3),
    }

    weighted_sum = 0.0
    total_weight = 0.0

    for score, weight in components.values():
        if score is not None:
            weighted_sum += score * weight
            total_weight += weight

    if total_weight == 0:
        return None

    return round(weighted_sum / total_weight, 1)


def classify_location_risk(score: float) -> tuple[str, str]:
    if score >= 75:
        return "Low Risk", "🟢"
    elif score >= 50:
        return "Moderate Risk", "🟡"
    else:
        return "Elevated Risk", "🔴"


# =====================================================
# Public policy entry point
# =====================================================
def assess_location_risk(
    crime_percentile: Optional[float],
    irsd_decile: Optional[int],
    irsad_decile: Optional[int],
) -> Dict:
    """
    Location / Neighbourhood risk policy.

    Designed for:
    - Partial data tolerance
    - Analyst-readable explanations
    - Credit memo–ready output
    """

    # -----------------------------
    # Step 1: Convert inputs
    # -----------------------------
    crime_score = crime_score_from_percentile(crime_percentile)

    irsd_score = _lookup_score(
        _load_decile_scoring_table("IRSD_decile"),
        "IRSD_decile",
        irsd_decile,
    )

    irsad_score = _lookup_score(
        _load_decile_scoring_table("IRSAD_decile"),
        "IRSAD_decile",
        irsad_decile,
    )

    # -----------------------------
    # Step 2: Composite score
    # -----------------------------
    score = calculate_location_score(
        crime_score,
        irsd_score,
        irsad_score,
    )

    if score is None:
        return {
            "risk_name": "Location",
            "score": None,
            "label": "Unknown",
            "icon": "⚪",
            "flags": ["INSUFFICIENT_DATA"],
            "requires_manual_review": True,
            "rationale": "Insufficient data to assess location risk.",
        }


    # -----------------------------
    # Step 3: Classification
    # -----------------------------
    label, icon = classify_location_risk(score)

    # -----------------------------
    # Step 4: Rationale
    # -----------------------------
    rationale_parts = [
        crime_rationale(crime_percentile),
    ]

    if irsd_score is not None:
        rationale_parts.append(
            f"IRSD decile {irsd_decile} reflects relative socio-economic disadvantage."
        )

    if irsad_score is not None:
        rationale_parts.append(
            f"IRSAD decile {irsad_decile} indicates overall advantage/disadvantage profile."
        )

    rationale = " ".join(rationale_parts)

    # -----------------------------
    # Step 5: Output
    # -----------------------------
    return {
        "risk_name": "Location",
        "score": score,
        "label": label,
        "icon": icon,
        "flags": [] if all(v is not None for v in [crime_score, irsd_score, irsad_score])
        else ["PARTIAL_DATA_USED"],
        "requires_manual_review": not all(
            v is not None for v in [crime_score, irsd_score, irsad_score]
        ),
        "rationale": rationale,
    }