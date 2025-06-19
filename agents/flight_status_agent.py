import requests
from config.settings import API_KEY

class FlightStatusAgent:
    def run(self, flight_number: str) -> str:
        response = requests.get(
            "http://api.aviationstack.com/v1/flights",
            params={"access_key": API_KEY, "flight_iata": flight_number}
        )
        data = response.json().get("data", [])
        if not data:
            return f"❌ No info found for flight {flight_number}."
        f = data[0]
        return (
            f"✈️ Flight {flight_number}: {f['departure']['airport']} → "
            f"{f['arrival']['airport']}, status: {f['flight_status']}."
        )
