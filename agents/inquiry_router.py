import re
from agents.flight_status_agent import FlightStatusAgent
from agents.flight_analytics_agent import FlightAnalyticsAgent

class InquiryRouter:
    def route(self, query: str) -> str:
        match = re.search(r"\b([A-Z]{2}\d{3,4})\b", query.strip().upper())
        if match:
            return FlightStatusAgent().run(match.group(1))
        return FlightAnalyticsAgent().run(query)
