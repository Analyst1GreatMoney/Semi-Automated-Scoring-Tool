import pandas as pd
from pathlib import Path

# -----------------------------------------------------
# Resolve data directory robustly
# -----------------------------------------------------
DATA_DIR = Path(__file__).resolve().parent


# -----------------------------------------------------
# Individual loaders
# -----------------------------------------------------
def load_crime_data():
    path = DATA_DIR / "crime.csv"
    if not path.exists():
        # graceful fallback
        return pd.DataFrame()
    return pd.read_csv(path)


def load_seifa_data():
    path = DATA_DIR / "seifa.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_lga_irsad_data():
    path = DATA_DIR / "lga_irsad.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


# -----------------------------------------------------
# Public dataset bundle
# -----------------------------------------------------
def get_location_datasets():
    return {
        "crime": load_crime_data(),
        "seifa": load_seifa_data(),
        "lga_irsad": load_lga_irsad_data(),
    }
