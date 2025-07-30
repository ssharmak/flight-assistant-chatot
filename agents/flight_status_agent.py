import re
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from config.settings import API_KEY, PROJECT_ID, BQ_DATASET, BQ_TABLE
from google.cloud.bigquery import ScalarQueryParameter, QueryJobConfig

class FlightStatusAgent:
    def run(self, flight_number: str) -> str:
        """
        Main entry point for the FlightStatusAgent.
        Validates the flight number, fetches flight data from BigQuery,
        and returns a formatted status response.
        """
        # Clean and standardize input
        flight_number = flight_number.strip().upper()

        # Validate the format of the flight number
        if not re.match(r'^[A-Z0-9]+$', flight_number):
            return "❌ Please enter a valid flight number (letters and/or digits only)."

        # Attempt to fetch flight data from BigQuery
        try:
            record = self.fetch_flight_from_bigquery(flight_number)
            if record:
                return self.format_response(record)
            else:
                return f"❌ No flight data found for flight number {flight_number} in BigQuery."
        except Exception as e:
            return f"❌ Error while accessing flight data: {str(e)}"

    def fetch_flight_from_bigquery(self, flight_number: str) -> dict:
        """
        Queries BigQuery to fetch flight information matching the given flight number.

        Parameters:
        - flight_number (str): The sanitized flight number to query.

        Returns:
        - dict: Dictionary of flight details if found, else None.
        """
        # Initialize BigQuery client
        client = bigquery.Client()

        # Fully-qualified table reference: project.dataset.table
        full_table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

        # SQL query with parameterized flight number for security
        query = f"""
            SELECT * FROM `{full_table_id}`
            WHERE UPPER(flight_number) = @flight_number
            LIMIT 1
        """

        # Configure query parameters to prevent SQL injection
        job_config = QueryJobConfig(
            query_parameters=[
                ScalarQueryParameter("flight_number", "STRING", flight_number)
            ]
        )

        # Execute the query and retrieve results
        results = client.query(query, job_config=job_config).result()

        # Return the first matching row as a dictionary (if any)
        for row in results:
            return dict(row)

        return None  # No matching record found

    def format_response(self, record: dict) -> str:
        """
        Formats the BigQuery record into a user-friendly response string.

        Parameters:
        - record (dict): The flight information retrieved from BigQuery.

        Returns:
        - str: A formatted string containing flight status details.
        """
        # Create a nicely formatted response using available fields
        response = (
            f"✈️ **Flight Details:**\n"
            f"• Flight Number: {record.get('flight_number', 'N/A')}\n"
            f"• Departure: {record.get('departure_airport', 'N/A')} at {record.get('departure_time', 'N/A')}\n"
            f"• Arrival: {record.get('arrival_airport', 'N/A')} at {record.get('arrival_time', 'N/A')}\n"
            f"• Status: {record.get('status', 'N/A')}\n"
        )
        return response
