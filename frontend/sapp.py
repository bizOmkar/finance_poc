import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Finance Analyst Assistant - Vedanta",
    layout="wide",
    page_icon="💹"
)

# --- Header Section with Horizontal Line Between Logo and Client Name ---
header_col1, header_col2 = st.columns([0.2, 0.8])

with header_col1:
    st.image(r"C:\Bizmetric\GENAI_POC\copy_vedanta\frontend\assets\bm_logo.png", width=60)  # <-- Bizmetric logo here

with header_col2:
    st.markdown(
        """
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <h1 style='color:#003366; font-size:32px; margin: 0;'>Finance Analyst Assistant</h1>
            <h3 style='color:gray; font-size:18px; margin: 0;'>Vedanta</h3>
        </div>
        <hr style='margin-top:8px; border: 0.5px solid lightgray;' />
        """,
        unsafe_allow_html=True
    )

# --- Helper Function to handle API calls safely ---
def safe_api_post(url, payload):
    try:
        response = requests.post(url, json=payload)

        if response.status_code != 200:
            st.error(f"❌ Server Error: {response.status_code}")
            return None

        res_json = response.json()

        if "response" not in res_json:
            st.error("❌ 'response' field missing in API output")
            return None

        return res_json["response"]

    except Exception as e:
        st.error(f"❌ API Call failed: {e}")
        return None

# --- Query Section ---
st.subheader("Ask a Question")

query = st.text_input(" Ask a question about your financial data", placeholder="e.g. Alumina cost in quarter 3")

if st.button("Submit Query"):
    with st.spinner("Analyzing your query..."):
        result = safe_api_post("http://127.0.0.1:8080/query", {"query": query})

        if result:
            if result["type"] == "image":
                st.image(result["data"], caption="Generated Chart")
            elif result["type"] == "text":
                st.markdown(result["data"])
            else:
                st.warning("⚠️ Unknown response type received.")

# --- EBITDA Walk Section ---
st.subheader("EBITDA Walk Chart")

source_quarter = st.selectbox("Select Source Quarter", ["Q1FY24", "Q2FY24", "Q3FY24", "Q4FY24"])
target_quarter = st.selectbox("Select Target Quarter", ["Q1FY24", "Q2FY24", "Q3FY24", "Q4FY24"])

if st.button("Plot EBITDA Walk"):
    with st.spinner("Generating Waterfall Chart..."):
        result = safe_api_post(
            "http://127.0.0.1:8080/ebitda-walk-selection",
            {"source_quarter": source_quarter, "target_quarter": target_quarter}
        )

        if result:
            if result["type"] == "image":
                st.image(result["data"], caption=f"EBITDA Walk: {source_quarter} to {target_quarter}")
            elif result["type"] == "text":
                st.markdown(result["data"])
            else:
                st.warning("⚠️ Unknown response type received.")

