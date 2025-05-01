# import streamlit as st
# import requests

# st.title("Finance Analyst Assistant")

# query = st.text_input("Ask a question about your financial data")

# if st.button("Submit"):
#     response = requests.post("http://127.0.0.1:8001/query", json={"query": query})
#     result = response.json()["response"]

#     if isinstance(result, dict) and "type" in result:
#         if result["type"] == "image":
#             st.image(result["data"])
#         elif result["type"] == "text":
#             st.markdown(result["data"])
#         else:
#             st.warning("Unknown response type")
#     else:
#         st.error("Unexpected response format")
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
    st.image("assets/bm_logo.png", width=60)  # <-- Bizmetric logo here

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

# --- Input Section ---
query = st.text_input(" Ask a question about your financial data", placeholder="e.g. Show EBITDA walk from Q1 to Q3")

if st.button(" Submit"):
    with st.spinner("Analyzing your data..."):
        response = requests.post("http://127.0.0.1:8001/query", json={"query": query})
        result = response.json()["response"]

    if isinstance(result, dict) and "type" in result:
        if result["type"] == "image":
            st.image(result["data"], caption="Generated Chart")
        elif result["type"] == "text":
            st.markdown(result["data"])
        else:
            st.warning("⚠️ The response type is unknown.")
    else:
        st.error("❌ Unexpected response format from the backend.")


