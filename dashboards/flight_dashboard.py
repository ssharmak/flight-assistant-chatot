import os
import streamlit as st
from google.cloud import bigquery
from dotenv import load_dotenv
import pandas as pd

# Load env
load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID = os.getenv("TABLE_ID")
FULL_TABLE = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# BigQuery client
client = bigquery.Client()

# UI Layout
st.set_page_config("Flight Insights", layout="wide")
st.title("✈️ Flight Dashboard & Chatbot")
st.markdown("### Live Flight Table (Latest 50)")

@st.cache_data(ttl=300)
def load_recent():
    df = client.query(f"""
        SELECT flight_date, airline_name, flight_number,
               departure_airport, arrival_airport, status,
               scheduled_departure
        FROM `{FULL_TABLE}`
        ORDER BY scheduled_departure DESC
        LIMIT 50
    """).to_dataframe()
    return df

st.dataframe(load_recent(), use_container_width=True)

st.markdown("---")
st.header("💬 Ask Flight Info")

user_q = st.text_input("Your Query (e.g., flight AA123 status, arrivals from JFK)", "")

if user_q:
    st.markdown("**Response:**")
    # Basic intent detection
    import re
    flight_match = re.search(r"\b([A-Z]{2}\d{3,4})\b", user_q.upper())
    if flight_match:
        # Flight status query flow
        num = flight_match.group(1)
        sql = f"""
          SELECT flight_date, departure_airport, arrival_airport,
                 status, scheduled_departure
          FROM `{FULL_TABLE}`
          WHERE flight_number = '{num}'
          ORDER BY scheduled_departure DESC
          LIMIT 1
        """
    else:
        # Route arrivals/departures query
        route_match = re.search(r"\bfrom\s*([A-Z]{3})", user_q.upper())
        loc = route_match.group(1) if route_match else None
        if loc:
            sql = f"""
              SELECT flight_date, airline_name, flight_number,
                     departure_airport, arrival_airport, status
              FROM `{FULL_TABLE}`
              WHERE departure_airport LIKE '%{loc}%' 
                OR arrival_airport LIKE '%{loc}%'
              ORDER BY flight_date DESC
              LIMIT 10
            """
        else:
            sql = None

    if sql:
        try:
            result = client.query(sql).to_dataframe()
            if not result.empty:
                st.table(result)
            else:
                st.write("❌ No matching flights found.")
        except Exception as e:
            st.write("❌ Error querying BigQuery:")
            st.exception(e)
    else:
        st.write("🤖 I didn't understand. Try 'flight XX1234' or 'from JFK'.")
