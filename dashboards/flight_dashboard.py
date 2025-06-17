import streamlit as st
import pandas as pd
import subprocess
import sys
from agents.inquiry_router import get_response
from processor.analyze_flights import analyze_weekly_data

# Set page configuration
st.set_page_config(page_title="Flight Dashboard", layout="wide")

# Title
st.title("✈️ Flight Data & Chat Assistant")

# Sidebar – Flight Data Fetching
st.sidebar.header("📅 Fetch Flight Data")
date_range = st.sidebar.date_input("Select start and end dates", [])

if len(date_range) == 2:
    start, end = date_range
    if st.sidebar.button("Fetch Flights"):
        with st.spinner("Fetching flight data and uploading to BigQuery..."):
            result = subprocess.run([
                sys.executable,
                "scripts/fetch_and_upload.py",
                "--start", start.isoformat(),
                "--end", end.isoformat()
            ])
        if result.returncode == 0:
            st.success("✅ Flights fetched and uploaded successfully.")
        else:
            st.error("❌ Failed to fetch or upload flight data.")
else:
    st.sidebar.info("Please select both start and end dates.")

# Divider
st.markdown("---")

# Flight Trends Section
st.subheader("📈 Flight Trends (Last 7 Days)")

try:
    df = analyze_weekly_data()
    if df.empty:
        st.warning("No data available to display.")
    else:
        st.dataframe(df)
        st.line_chart(df.set_index("flight_date")[["total_flights", "cancelled", "delayed"]])
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")

# Divider
st.markdown("---")

# Chatbot Section
st.subheader("🤖 Flight Assistant Chatbot")
user_input = st.text_input("Ask me about your flight status, schedule, or best route...")

if user_input:
    try:
        response = get_response(user_input)
        st.markdown(f"**Chatbot:** {response}")
    except Exception as e:
        st.error(f"❌ Chatbot error: {e}")
