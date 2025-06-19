from google.cloud import bigquery
import re
from config.settings import PROJECT_ID, BQ_DATASET, BQ_TABLE

class FlightAnalyticsAgent:
    """
    Agent class to handle flight route trend analytics using BigQuery.
    """

    def run(self, query: str) -> str:
        """
        Analyze flight trends based on user input like "DEL to BOM".

        Parameters:
            query (str): A natural language or semi-structured query containing airport codes.

        Returns:
            str: Formatted response with airline-wise flight frequency and average duration.
        """
        # Extract origin and destination IATA codes using regex (e.g., "DEL to BOM")
        m = re.search(r"\b([A-Z]{3})\s*to\s*([A-Z]{3})\b", query.upper())
        if not m:
            return "❓ Please use format like 'DEL to BOM'."

        origin, dest = m.group(1), m.group(2)

        # Create BigQuery client using project ID from config
        client = bigquery.Client(project=PROJECT_ID)
        table = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

        # Query: Count flights and calculate average duration between the two airports in the last 7 days
        sql = f"""
        SELECT 
            airline_name, 
            COUNT(*) AS flights,
            AVG(TIMESTAMP_DIFF(scheduled_arrival, scheduled_departure, MINUTE)) AS avg_duration
        FROM `{table}`
        WHERE 
            departure_airport LIKE '%{origin}%' AND
            arrival_airport LIKE '%{dest}%' AND
            flight_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        GROUP BY airline_name
        ORDER BY flights DESC
        LIMIT 3
        """

        # Execute the query and process results
        rows = client.query(sql).result()

        if rows.total_rows == 0:
            return f"No flights found from {origin} to {dest} in the last 7 days."

        # Format the result into a user-friendly message
        msg = f"📊 Trend {origin}→{dest} (last 7 days):\n"
        for row in rows:
            msg += f"{row.airline_name}: {row.flights} flights, avg duration ≈ {int(row.avg_duration)} min\n"
        return msg
