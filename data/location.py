import pandas as pd
from pathlib import Path

# =====================================================
# Data Access Layer – Location datasets
# =====================================================

DATA_DIR = Path(__file__).resolve().parent


# -----------------------------------------------------
# Internal CSV loader (private)
# -----------------------------------------------------
def _load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV file from the data directory.
    Returns empty DataFrame if file is missing.
    """
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


# -----------------------------------------------------
# Individual dataset loaders
# -----------------------------------------------------
def load_crime_data() -> pd.DataFrame:
    return _load_csv("crime.csv")


def load_seifa_data() -> pd.DataFrame:
    return _load_csv("seifa.csv")


def load_lga_irsad_data() -> pd.DataFrame:
    return _load_csv("lga_irsad.csv")


# -----------------------------------------------------
# Public dataset bundle
# -----------------------------------------------------
def get_location_datasets() -> dict[str, pd.DataFrame]:
    """
    Load all location-related datasets.
    """
    return {
        "crime": load_crime_data(),
        "seifa": load_seifa_data(),
        "lga_irsad": load_lga_irsad_data(),
    }


# -----------------------------------------------------
# Row-level access helpers
# -----------------------------------------------------
def get_suburb_row(
    df: pd.DataFrame,
    suburb_key: str,
    key_col: str = "SUBURB_KEY",
):
    """
    Safely retrieve a suburb-level row from a dataset.

    Parameters
    ----------
    df : DataFrame
        Dataset to search.
    suburb_key : str
        Normalised suburb key.
    key_col : str, default 'SUBURB_KEY'
        Column name used for matching.

    Returns
    -------
    Series or None
    """
    if df is None or df.empty:
        return None

    if key_col not in df.columns:
        return None

    filtered = df[df[key_col] == suburb_key]
    if filtered.empty:
        return None

    return filtered.iloc[0]


def get_location_inputs(datasets: dict, suburb_key: str) -> dict:
    """
    Collect all location-related raw inputs required for policy assessment.
    """
    return {
        "crime": get_suburb_row(datasets.get("crime"), suburb_key),
        "seifa": get_suburb_row(datasets.get("seifa"), suburb_key),
        "lga": get_suburb_row(datasets.get("lga_irsad"), suburb_key),
    }
