import streamlit as st

# ----- Page Configuration -----
st.set_page_config(
    page_title="Semi-Automated Borrower Scoring Tool",
    page_icon="📊",
    layout="centered"
)

# ----- Header -----
st.title("📊 Semi-Automated Borrower Scoring Tool (Prototype)")
st.write("Welcome! This is Version 1 of the internal scoring system designed to help standardise borrower assessments using the Five C lending framework.")

# ----- Intro Section -----
st.markdown("""
### 👋 Hello!
This tool is currently in its **early prototype stage**, and aims to:

- Provide a **simple and consistent way** to evaluate borrowers  
- Begin automating the **Five C** credit assessment model  
- Test scoring logic and user interface flow  
- Lay the foundation for a more complete tool in later versions  

Version 1 starts with implementing **one of the Five Cs** as a proof-of-concept.
""")

# ----- Divider -----
st.markdown("---")

st.subheader("💡 What's coming next?")
st.markdown("""
In future versions, the tool will expand to include:

- All Five C scoring components  
- A combined final score and risk grade  
- Configurable scoring rules (editable without coding)  
- A clean multi-page Streamlit interface  
""")

# ----- Footer -----
st.markdown("---")
st.caption("Prototype V1 • Developed by Frank • Streamlit Implementation")
