import os
import requests
from google.cloud import bigquery
from dotenv import load_dotenv
from datetime import datetime
import time

# Load environment variables
load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
BQ_DATASET = os.getenv("DATASET_ID")
BQ_TABLE = os.getenv("TABLE_ID")
TABLE_ID = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

if not all([API_KEY, PROJECT_ID, BQ_DATASET, BQ_TABLE]):
    raise ValueError("❌ Missing one or more environment variables.")

BASE_URL = "http://api.aviationstack.com/v1/flights"

def fetch_flights(limit=100, offset=0):
    params = {
        "access_key": API_KEY,
        "limit": limit,
        "offset": offset
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json().get("data", [])

def parse_ts(ts):
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else None
        return dt.isoformat() if dt else None
    except Exception:
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
    rows = [format_row(item) for item in flights if item and item.get("flight", {}).get("iata")]

    if not rows:
        print("⚠️ No valid rows to upload.")
        return

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

    if not errors:
        print(f"✅ Inserted {len(rows)} rows successfully.")
    else:
        print("❌ Insert errors:", errors)

if __name__ == "__main__":
    try:
        all_flights = []
        print("📡 Fetching first 100 flights...")
        all_flights += fetch_flights(limit=100, offset=0)
        time.sleep(1)  # Avoid hitting rate limit

        print("📡 Fetching next 100 flights...")
        all_flights += fetch_flights(limit=100, offset=100)

        print(f"📦 Retrieved {len(all_flights)} flights. Uploading to BigQuery...")
        upload_to_bigquery(all_flights)

    except Exception as e:
        print("❌ Failed:", e)
