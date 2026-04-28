import streamlit as st
import requests

# ======================
# Page setup
# ======================
st.set_page_config(
    page_title="Community Audit Tool",
    layout="wide"
)

st.title("Community Audit Tool")
st.caption("No login • Works on Mac & Windows")

# ======================
# BACKEND URL
# ======================
# 👉 REPLACE this with your actual Render backend URL
BACKEND_URL = "https://community-audit-backend.onrender.com"

# ======================
# PRODUCT → SECTION → URL MAPPING
# ======================
PRODUCTS = {
    "Acrobat": {
        "Questions": "https://community.adobe.com/questions-9/",
        "Bugs": "https://community.adobe.com/bugs-9/",
        "Feature Requests": "https://community.adobe.com/feature-requests-9/"
    },
    "Photoshop": {
        "Questions": "https://community.adobe.com/questions-713/",
        "Bugs": "https://community.adobe.com/bugs-713/",
        "Feature Requests": "https://community.adobe.com/feature-requests-713/"
    },
    "Illustrator": {
        "Questions": "https://community.adobe.com/questions-651/",
        "Bugs": "https://community.adobe.com/bugs-651/",
        "Feature Requests": "https://community.adobe.com/feature-requests-651/"
    }
    # ✅ You will add the rest of your products here later
}

# ======================
# UI CONTROLS
# ======================
col1, col2, col3 = st.columns(3)

with col1:
    product = st.selectbox("Select Product", list(PRODUCTS.keys()))

with col2:
    section = st.selectbox(
        "Select Section",
        list(PRODUCTS[product].keys())
    )

with col3:
    st.markdown("### Thread Criteria")

filter_type = st.selectbox(
    "Primary Filter",
    ["all", "answered", "unanswered"]
)

extra_criteria = st.multiselect(
    "Additional criteria (optional)",
    [
        "No replies",
        "No accepted answer",
        "Older than 7 days",
        "Older than 14 days"
    ]
)

date_col1, date_col2 = st.columns(2)
with date_col1:
    start_date = st.date_input("Start Date")

with date_col2:
    end_date = st.date_input("End Date")


# ======================
# RUN BUTTON
# ======================
# ======================
# RUN BUTTON
# ======================

st.divider()
st.subheader("Run")

if st.button("🚀 Run Audit", use_container_width=True):
    board_url = PRODUCTS[product][section]

    payload = {
        "board": board_url,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "filter": filter_type,
        "extra_criteria": extra_criteria
    }

    st.info("Sending request to backend...")

    try:
        response = requests.post(
            f"{BACKEND_URL}/run",
            json=payload,
            timeout=60
        )
        st.success("Response received ✅")


st.info("Sending request to backend...")

response = requests.post(
    f"{BACKEND_URL}/run",
    json=payload,
    timeout=60
)

st.subheader("Raw backend response")

st.text(f"Status code: {response.status_code}")
st.text("Headers:")
st.text(dict(response.headers))

st.text("Body:")
st.text(response.text)

# ✅ Parse JSON only if possible
try:
    st.subheader("Parsed JSON")
    st.json(response.json())
except Exception as e:
    st.warning(f"JSON parse failed: {e}")

    except Exception as e:
        st.error(f"Could not reach backend: {e}")


