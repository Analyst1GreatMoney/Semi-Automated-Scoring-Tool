# data/loaders.py
import pandas as pd
import streamlit as st
from utils.paths import DATA_DIR
from data.normalisation import normalise_suburb_name, normalise_lga_name

@st.cache_data
def load_crime_data():
    path = BASE_DIR / "doc" / "Collateral" / "data" / \
        "suburb_crime_risk_12m_2024_07_to_2025_06.csv"
    df = pd.read_csv(path)
    df["SUBURB_KEY"] = df["Suburb"].apply(normalise_suburb_name)
    df["crime_percentile"] = (
        df["crime_12m"].rank(pct=True, ascending=True) * 100
    )
    return df


@st.cache_data
def load_seifa_data():
    path = BASE_DIR / "doc" / "Collateral" / "data" / \
        "suburb_irsd_irsad.csv"
    df = pd.read_csv(path)
    df["SUBURB_KEY"] = df["suburb_name"].apply(normalise_suburb_name)
    return df

@st.cache_data
def load_lga_irsad_data():
    """
    Load LGA-level IRSAD data (2021)
    """
    path = BASE_DIR / "doc" / "Collateral" / "data" / "lga_irsad_2021_clean.csv"
    df = pd.read_csv(path)

    # Normalise LGA names for matching
    df["LGA_KEY"] = df["lga_name"].apply(normalise_lga_name)

    return df
