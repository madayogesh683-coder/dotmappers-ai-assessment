import streamlit as st
import requests

st.set_page_config(
    page_title="Support Ticket AI",
    page_icon="🎫",
    layout="wide"
)

st.title("🎫 Support Ticket AI")
st.write("AI-powered support ticket analysis")

# API URL
API_URL = "http://127.0.0.1:8001"

# Get health information
try:
    health = requests.get(f"{API_URL}/health").json()
    total_tickets = health["total_tickets"]

    st.metric("Total Tickets", total_tickets)

except Exception:
    st.error("FastAPI server is not running.")

st.divider()

# Natural language query
st.subheader("Ask about support tickets")

question = st.text_input(
    "Enter your question:",
    placeholder="Example: How many open tickets are there?"
)

if st.button("Ask"):
    if question:
        try:
            response = requests.get(
                f"{API_URL}/query",
                params={"question": question}
            )

            result = response.json()

            st.success(result["answer"])

        except Exception as e:
            st.error(f"Error connecting to API: {e}")
    else:
        st.warning("Please enter a question.")

st.divider()

# Anomaly detection
st.subheader("🚨 Ticket Anomalies")

if st.button("Detect Anomalies"):
    try:
        response = requests.get(f"{API_URL}/anomalies")
        result = response.json()

        st.write(
            f"**Total anomalies detected: "
            f"{result['total_anomalies']}**"
        )

        if result["anomalies"]:
            st.dataframe(result["anomalies"])

    except Exception as e:
        st.error(f"Error connecting to API: {e}")