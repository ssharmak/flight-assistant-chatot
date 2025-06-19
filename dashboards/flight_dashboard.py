import os
import streamlit as st
from google.cloud import bigquery
from dotenv import load_dotenv
import pandas as pd
import requests
from datetime import datetime
import time

# Load environment variables
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
BQ_DATASET = os.getenv("DATASET_ID")
BQ_TABLE = os.getenv("TABLE_ID")
TABLE_ID = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
BASE_URL = "http://api.aviationstack.com/v1/flights"

# ----- Styling -----
st.set_page_config(layout="wide", page_title="✈️ Flight Tracker Dashboard")

def set_bg():
    st.markdown("""
        <style>
        .stApp {
             background-image: url("https://wallpapers.com/images/hd/planes-4k-ultra-hd-ypebdpcfccod2b8t.jpg");
            background-size: cover;
            background-size: cover;
            background-attachment: fixed;
            color: white;
        }
        .title {
            font-size: 48px;
            font-weight: 800;
            color: #ffffff;
            text-shadow: 2px 2px 4px #000;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

set_bg()
st.markdown('<div class="title">✈️ Flight Dashboard (Live Update)</div>', unsafe_allow_html=True)

# ----- Utility Functions -----
def parse_ts(ts):
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else None
        return dt.isoformat() if dt else None
    except:
        return None

def format_row(item):
    return {
        "flight_date": item.get("flight_date"),
        "airline_name": item.get("airline", {}).get("name"),
        "flight_number": item.get("flight", {}).get("iata"),
        "departure_airport": item.get("departure", {}).get("airport"),
        "arrival_airport": item.get("arrival", {}).get("airport"),
        "status": item.get("flight_status"),
        "scheduled_departure": parse_ts(item.get("departure", {}).get("scheduled")),
        "scheduled_arrival": parse_ts(item.get("arrival", {}).get("scheduled")),
    }

def refresh_data_from_aviationstack():
    try:
        all_flights = []
        for offset in [0, 100]:
            params = {"access_key": API_KEY, "limit": 100, "offset": offset}
            r = requests.get(BASE_URL, params=params)
            r.raise_for_status()
            all_flights += r.json().get("data", [])
            time.sleep(1)

        rows = [format_row(f) for f in all_flights if f and f.get("flight", {}).get("iata")]
        client = bigquery.Client()
        unique_keys = {(r['flight_date'], r['flight_number']) for r in rows if r['flight_date'] and r['flight_number']}

        for flight_date, flight_number in unique_keys:
            delete_sql = f"""
                DELETE FROM `{TABLE_ID}`
                WHERE flight_date = @flight_date AND flight_number = @flight_number
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("flight_date", "DATE", flight_date),
                    bigquery.ScalarQueryParameter("flight_number", "STRING", flight_number),
                ]
            )
            client.query(delete_sql, job_config=job_config).result()

        errors = client.insert_rows_json(TABLE_ID, rows)
        return len(rows), errors
    except Exception as e:
        return 0, str(e)

# ✅ Cached data loader
@st.cache_data(show_spinner=False)
def load_data_from_bigquery():
    client = bigquery.Client()
    query = f"SELECT * FROM `{TABLE_ID}` ORDER BY scheduled_departure DESC"
    return client.query(query).to_dataframe()

# ----- Refresh Button -----
if st.button("🔁 Refresh Flight Data from Aviationstack"):
    with st.spinner("Fetching live data from API..."):
        inserted, errors = refresh_data_from_aviationstack()
        st.cache_data.clear()  # clear cached data after refresh
        if errors == []:
            st.success(f"✅ {inserted} rows inserted into BigQuery.")
        else:
            st.error(f"❌ Error uploading data: {errors}")

# ----- Load and Display Data -----
try:
    df = load_data_from_bigquery()

    if df.empty:
        st.warning("No data available.")
    else:
        st.markdown("### 📋 Flight Table")
        st.dataframe(df, use_container_width=True)

        st.markdown("### 🧭 Pie Chart: Status")
        counts = df["status"].value_counts()
        st.plotly_chart({
            "data": [{
                "type": "pie",
                "labels": counts.index.tolist(),
                "values": counts.values.tolist()
            }],
            "layout": {
                "title": "Flight Status Overview",
                "paper_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"}
            }
        }, use_container_width=True)

except Exception as e:
    st.error(f"❌ Failed to load dashboard: {e}")
