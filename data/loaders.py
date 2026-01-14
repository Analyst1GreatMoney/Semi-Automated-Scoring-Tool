import pandas as pd
import streamlit as st
from pathlib import Path

from data.normalisation import (
    normalise_suburb_name,
    normalise_lga_name,
)

# =====================================================
# Project root resolution
# =====================================================
# data/loaders.py → data → project root
BASE_DIR = Path(__file__).resolve().parents[1]

COLLATERAL_DATA_DIR = BASE_DIR / "doc" / "Collateral" / "data"

if not COLLATERAL_DATA_DIR.exists():
    raise FileNotFoundError(
        f"Collateral data directory not found: {COLLATERAL_DATA_DIR}"
    )

# =====================================================
# Crime data (suburb-level)
# =====================================================
@st.cache_data
def load_crime_data() -> pd.DataFrame:
    """
    Load suburb-level crime risk data and derive percentile.
    """
    path = next(
        COLLATERAL_DATA_DIR.glob("suburb_crime_risk*.csv"),
        None,
    )

    if path is None or not path.exists():
        raise FileNotFoundError(
            "Suburb crime risk CSV not found in Collateral/data"
        )

    df = pd.read_csv(path)

    required_cols = {"Suburb", "crime_12m"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"Crime CSV missing required columns: {required_cols}"
        )

    # 🔑 Canonical suburb key (唯一标准)
    df["SUBURB_KEY"] = df["Suburb"].astype(str).apply(normalise_suburb_name)

    # Higher percentile = safer suburb
    df["crime_percentile"] = (
        df["crime_12m"].rank(pct=True, ascending=True) * 100
    )

    return df


# =====================================================
# SEIFA (IRSD / IRSAD) – suburb-level
# =====================================================
@st.cache_data
def load_seifa_data() -> pd.DataFrame:
    """
    Load suburb-level IRSD / IRSAD data.
    """
    path = COLLATERAL_DATA_DIR / "suburb_irsd_irsad.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"SEIFA suburb file not found: {path}"
        )

    df = pd.read_csv(path)

    required_cols = {
        "suburb_name",
        "IRSD_decile",
        "IRSAD_decile",
    }
    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"SEIFA CSV missing required columns: {required_cols}"
        )

    # 🔑 Canonical suburb key（必须和 crime 用同一个 normalise）
    df["SUBURB_KEY"] = df["suburb_name"].astype(str).apply(
        normalise_suburb_name
    )

    return df


# =====================================================
# LGA IRSAD – LGA-level
# =====================================================
@st.cache_data
def load_lga_irsad_data() -> pd.DataFrame:
    """
    Load LGA-level IRSAD data (ABS 2021).
    """
    path = COLLATERAL_DATA_DIR / "lga_irsad_2021_clean.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"LGA IRSAD file not found: {path}"
        )

    df = pd.read_csv(path)

    if "lga_name" not in df.columns:
        raise ValueError("LGA IRSAD CSV missing lga_name column")

    # 🔑 Canonical LGA key
    df["LGA_KEY"] = df["lga_name"].astype(str).apply(normalise_lga_name)

    return df


# =====================================================
# Public dataset bundle
# =====================================================
def get_location_datasets() -> dict[str, pd.DataFrame]:
    """
    Load all datasets required for location / neighbourhood risk.
    """
    return {
        "crime": load_crime_data(),
        "seifa": load_seifa_data(),
        "lga_irsad": load_lga_irsad_data(),
    }


# =====================================================
# Row-level access helpers
# =====================================================
def _get_row_by_key(
    df: pd.DataFrame,
    key_col: str,
    key: str | None,
):
    if df is None or df.empty or key is None:
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
    datasets: dict,
    suburb_key: str,
    lga_key: str | None = None,
) -> dict:
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
