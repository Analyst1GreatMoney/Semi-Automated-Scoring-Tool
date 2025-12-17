import streamlit as st

def init_session_state():
    defaults = {
        "input_suburb": "",
        "input_lga": "",
        "marketability": None,
        "run_collateral_assessment": False,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
