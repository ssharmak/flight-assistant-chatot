from google.cloud import bigquery
import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
DATASET = os.getenv("BQ_DATASET")
TABLE = os.getenv("BQ_TABLE")

class FlightStatusAgent:
    def run(self, flight_number):
        client = bigquery.Client()
        query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE flight_number = @flight_number
        ORDER BY departure_scheduled DESC
        LIMIT 1
        """
       
