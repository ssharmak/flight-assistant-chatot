import re
from agents.flight_status_agent import FlightStatusAgent
from agents.flight_analytics_agent import FlightAnalyticsAgent

class InquiryRouter:
    def route(self, query: str) -> str:
        query_upper = query.strip().upper()

        # --- Flight Number Pattern (Flexible) ---
        # Matches 2–3 alphanumeric + 1–4 digits or any mix with optional trailing letters
        flight_pattern = re.search(r'\b([A-Z0-9]{2,4}\d{1,4}[A-Z]?)\b', query_upper)

        if flight_pattern:
            flight_number = flight_pattern.group(1)
            response = FlightStatusAgent().run(flight_number)

            if "No information found" not in response:
                return response

        # --- Flight Route (e.g., BLR to DEL) ---
        route_pattern = re.search(r'\b([A-Z]{3})\s*to\s*([A-Z]{3})\b', query_upper)
        if route_pattern:
            return FlightAnalyticsAgent().run(query_upper)

        # --- Fallback: Nothing recognized ---
        return "❓ Sorry, I couldn't identify a valid flight number or route in your query."
