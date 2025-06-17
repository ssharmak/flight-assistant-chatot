import re
from agents.flight_status_agent import FlightStatusAgent
from agents.flight_analytics_agent import FlightAnalyticsAgent  

class InquiryRouter:
    def __init__(self):
        self.status_agent = FlightStatusAgent()
        self.analytics_agent = FlightAnalyticsAgent()

    def get_response(self, query: str) -> str:
        query = query.strip()
        # Check for flight number format (e.g., AI202, EK528)
        match = re.search(r"\b([A-Z]{2}\d{3,4})\b", query.upper())
        if match:
            return self.status_agent.run(match.group(1))

        # Check for route format (e.g., DEL to BOM)
        match = re.search(r"\b([A-Z]{3})\s+to\s+([A-Z]{3})\b", query.upper())
        if match:
            return self.analytics_agent.run(query)

        return "❓ Please ask about a flight number (e.g., AI202) or route (e.g., BLR to BOM)."

class InquiryRouter:
    def route(self, query: str) -> str:
        match = re.search(r"\b([A-Z]{2}\d{3,4})\b", query.strip().upper())
        if match:
            return FlightStatusAgent().run(match.group(1))
        return FlightAnalyticsAgent().run(query)

# ✅ Add this helper function
def get_response(query: str) -> str:
    return InquiryRouter().route(query)
