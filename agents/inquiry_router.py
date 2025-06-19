import re
from agents.flight_status_agent import FlightStatusAgent
from agents.flight_analytics_agent import FlightAnalyticsAgent

class InquiryRouter:
    def route(self, query: str) -> str:
        query_upper = query.strip().upper()

        # If flight number is mentioned (like AI202)
        match = re.search(r'\b([A-Z]{2}\d{2,4})\b', query_upper)
        if match:
            return FlightStatusAgent().run(match.group(1))

        # If route is mentioned (like BLR to DEL)
        match = re.search(r'\b([A-Z]{3})\s*to\s*([A-Z]{3})\b', query_upper)
        if match:
            return FlightAnalyticsAgent().run(query)

        return "❓ Sorry, I couldn't understand your query. Try something like 'AI202' or 'BLR to DEL'"
