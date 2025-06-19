import requests
from config.settings import API_KEY

class FlightStatusAgent:
    # Handles the retrieval of flight status details using Aviationstack API
    def run(self, flight_number: str) -> str:
        # Send a GET request to Aviationstack API to retrieve data by flight number (IATA code)
        response = requests.get(
            "http://api.aviationstack.com/v1/flights",
            params={"access_key": API_KEY, "flight_iata": flight_number}
        )

        # Extract flight data from the API response
        data = response.json().get("data", [])
        
        # Handle case where no data is returned for the given flight number
        if not data:
            return f"❌ No info found for flight {flight_number}."

        # Use the first matching flight (API may return multiple matches)
        f = data[0]
        
        # Format and return the flight information (departure, arrival, status)
        return (
            f"✈️ Flight {flight_number}: {f['departure']['airport']} → "
            f"{f['arrival']['airport']}, status: {f['flight_status']}."
        )
