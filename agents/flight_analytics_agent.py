from google.cloud import bigquery
import re
from config.settings import PROJECT_ID, BQ_DATASET, BQ_TABLE

class FlightAnalyticsAgent:
    def run(self, query: str) -> str:
        try:
            m = re.search(r"\b([A-Z]{3})\s*to\s*([A-Z]{3})\b", query.upper())
            if not m:
                return "❓ Please specify route like 'DEL to BOM'."
            
            origin, dest = m.group(1), m.group(2)
            client = bigquery.Client(project=PROJECT_ID)
            table = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

            sql = f"""
            SELECT airline_name, COUNT(*) AS flights,
                   AVG(TIMESTAMP_DIFF(scheduled_arrival, scheduled_departure, MINUTE)) AS avg_duration
            FROM `{table}`
            WHERE departure_airport LIKE '%{origin}%' AND arrival_airport LIKE '%{dest}%'
              AND flight_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
            GROUP BY airline_name
            ORDER BY flights DESC
            LIMIT 3
            """

            rows = client.query(sql).result()
            if rows.total_rows == 0:
                return f"📭 No flights found from {origin} to {dest} in the past 7 days."

            response = f"📊 Top flights {origin} → {dest} (past 7 days):\n"
            for row in rows:
                response += f"• {row.airline_name} - {row.flights} flights, avg duration ≈ {int(row.avg_duration)} min\n"
            return response
        except Exception as e:
            return f"⚠️ Error analyzing flights: {e}"
