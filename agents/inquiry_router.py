import re
from agents.flight_status_agent import FlightStatusAgent
from agents.flight_analytics_agent import FlightAnalyticsAgent

class InquiryRouter:
    # Main router class to interpret user's natural language query and
    # delegate to the appropriate agent (status or analytics)

    def route(self, query: str) -> str:
        # Normalize query by trimming whitespace and converting to uppercase
        query_upper = query.strip().upper()

        # --- Flight Status Handler ---
        # Check if the query contains a flight number (e.g., AI202 or 6E1234)
        # Flight numbers typically start with 2 letters followed by 2–4 digits
        match = re.search(r'\b([A-Z]{2}\d{2,4})\b', query_upper)
        if match:
            return FlightStatusAgent().run(match.group(1))  # Call status agent

        # --- Flight Route Analytics Handler ---
        # Check if the query mentions a route like "BLR to DEL"
        match = re.search(r'\b([A-Z]{3})\s*to\s*([A-Z]{3})\b', query_upper)
        if match:
            return FlightAnalyticsAgent().run(query)  # Call analytics agent

        # Fallback: unrecognized query format
        return "❓ Sorry, I couldn't understand your query. Try something like 'AI202' or 'BLR to DEL'"
