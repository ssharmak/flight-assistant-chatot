import os
import requests
from datetime import datetime
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
DATASET = os.getenv("BQ_DATASET")
TABLE = os.getenv("BQ_TABLE")

def fetch_today_flights():
    today = datetime.today().strftime('%Y-%m-%d')
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&limit=100&flight_date={today}"
    print("📡 Fetching real-time flight data...")
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return data

def upload_to_bigquery(data):
    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"

    rows_to_insert = []
    for flight in data:
        try:
            rows_to_insert.append({
                "flight_date": flight.get("flight_date"),
                "flight_status": flight.get("flight_status"),
                "departure_airport": flight.get("departure", {}).get("airport"),
                "departure_iata": flight.get("departure", {}).get("iata"),
                "arrival_airport": flight.get("arrival", {}).get("airport"),
                "arrival_iata": flight.get("arrival", {}).get("iata"),
                "airline_name": flight.get("airline", {}).get("name"),
                "flight_number": flight.get("flight", {}).get("number"),
                "departure_scheduled": flight.get("departure", {}).get("scheduled"),
                "arrival_scheduled": flight.get("arrival", {}).get("scheduled")
            })
        except Exception as e:
            print(f"⚠️ Skipping invalid record: {e}")

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        print(f"❌ Upload failed with errors: {errors}")
    else:
        print(f"✅ Uploaded {len(rows_to_insert)} flights to BigQuery.")

def main():
    try:
        data = fetch_today_flights()
        if not data:
            print("⚠️ No flights found.")
        else:
            upload_to_bigquery(data)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
