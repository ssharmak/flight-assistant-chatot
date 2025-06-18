# scripts/fetch_and_upload.py

import requests
from google.cloud import bigquery
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")
BQ_TABLE = os.getenv("BQ_TABLE")
TABLE_ID = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

BASE_URL = "http://api.aviationstack.com/v1/flights"

def fetch_flights():
    params = {
        "access_key": API_KEY,
        "limit": 100
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json().get("data", [])

def parse_ts(ts):
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00')) if ts else None
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

def upload_to_bigquery(flights):
    client = bigquery.Client()
    rows = [format_row(item) for item in flights if item]
    if not rows:
        print("⚠️ No valid rows to upload.")
        return

    # Delete duplicates (flight_date + flight_number) before inserting
    unique_keys = {(r['flight_date'], r['flight_number']) for r in rows if r['flight_date'] and r['flight_number']}
    for flight_date, flight_number in unique_keys:
        delete_sql = f"""
        DELETE FROM `{TABLE_ID}`
        WHERE flight_date = '{flight_date}' AND flight_number = '{flight_number}'
        """
        client.query(delete_sql).result()

    errors = client.insert_rows_json(TABLE_ID, rows)
    if not errors:
        print(f"✅ Inserted {len(rows)} rows.")
    else:
        print("❌ Insert errors:", errors)

if __name__ == "__main__":
    try:
        print("📡 Fetching flight data...")
        flights = fetch_flights()
        print(f"📦 Retrieved {len(flights)} flights. Uploading to BigQuery...")
        upload_to_bigquery(flights)
    except Exception as e:
        print("❌ Failed:", e)
