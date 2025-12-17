# data/location.py
def get_location_datasets():
    return {
        "crime": load_crime_data(),
        "seifa": load_seifa_data(),
        "lga_irsad": load_lga_irsad_data(),
    }
