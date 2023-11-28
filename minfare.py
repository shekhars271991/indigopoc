import json

def extract_min_fare(json_data):
    results = json_data.get("response", {}).get("data", {}).get("results", [])
    all_fares = json_data.get("response", {}).get("data", {}).get("faresAvailable", {})

    min_fares = {}

    for result in results:
        trips = result.get("trips", [])

        for trip in trips:
            date = trip.get("date")
            fares = trip.get("journeysAvailableByMarket", {}).get("DEL|BOM", [])

            if not date or not fares:
                continue

            min_fare = float('inf')

            for fare in fares:
                passenger_fares = fare.get("fares", [])

                for passenger_fare in passenger_fares:
                    fare_av_key= passenger_fare.get("fareAvailabilityKey",{})
                    fare_tot = all_fares.get(fare_av_key,{}).get("totals",{}).get("fareTotal")
                    min_fare = min(min_fare, fare_tot)

            min_fares[date] = min_fare

    return min_fares

# Example usage
with open('/Users/shekharsuman/customers/indigo/pocpython/DEl-BOM-27-28-29.json', 'r') as file:
    flight_data = json.dumps(json.load(file))

data = json.loads(flight_data)
min_fares = extract_min_fare(data)

for date, fare in min_fares.items():
    print(f"Date: {date}, Minimum Fare: {fare}")
