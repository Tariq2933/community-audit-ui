import streamlit as st
import requests

st.set_page_config(
    page_title="Community Audit Tool",
    layout="wide"
)

st.title("🧪 Community Audit Tool (No Login)")

st.markdown("Select a board, choose a date range, and run the audit.")

# 👉 Replace this with YOUR Render backend URL
BACKEND_URL = "https://community-audit-backend.onrender.com"

boards = {
    "Acrobat – Questions": "https://community.adobe.com/questions-9/",
    "Acrobat – Feature Requests": "https://community.adobe.com/feature-requests-9/",
    "Acrobat – Bugs": "https://community.adobe.com/bugs-9/"
}

col1, col2, col3 = st.columns(3)

with col1:
    board_name = st.selectbox("Select board", list(boards.keys()))

with col2:
    start_date = st.date_input("Start date")

with col3:
    end_date = st.date_input("End date")

filter_type = st.radio(
    "Filter threads",
    ["all", "answered", "unanswered"],
    horizontal=True
)

if st.button("Run Audit"):
    payload = {
        "board": boards[board_name],
        "start_date": str(start_date),
        "end_date": str(end_date),
        "filter": filter_type
    }

    st.info("Sending request to backend...")

    try:
        r = requests.post(
            f"{BACKEND_URL}/run",
            json=payload,
            timeout=60
        )
        st.success("Response received ✅")
        st.json(r.json())

    except Exception as e:
        st.error(f"Error: {e}")
