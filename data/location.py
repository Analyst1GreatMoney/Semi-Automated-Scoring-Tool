# data/location.py
import pandas as pd
from typing import Dict, Optional

# 🔑 关键：把 loader 里的函数 re-export 出来
from data.loaders import get_location_datasets


# =====================================================
# Internal helper
# =====================================================
def _get_row_by_key(
    df: Optional[pd.DataFrame],
    key_col: str,
    key: str,
) -> Optional[pd.Series]:

    if df is None or df.empty:
        return None

    if key_col not in df.columns:
        return None

    matched = df[df[key_col] == key]
    if matched.empty:
        return None

    return matched.iloc[0]


# =====================================================
# Public API
# =====================================================
def get_location_inputs(
    datasets: Dict[str, pd.DataFrame],
    suburb_key: str,
    lga_key: Optional[str] = None,
) -> Dict[str, Optional[pd.Series]]:
    """
    Collect all raw inputs required for location risk assessment.
    """

    return {
        "crime": _get_row_by_key(
            datasets.get("crime"),
            "SUBURB_KEY",
            suburb_key,
        ),
        "seifa": _get_row_by_key(
            datasets.get("seifa"),
            "SUBURB_KEY",
            suburb_key,
        ),
        "lga": _get_row_by_key(
            datasets.get("lga_irsad"),
            "LGA_KEY",
            lga_key,
        ) if lga_key else None,
    }