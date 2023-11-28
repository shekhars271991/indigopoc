import json
import redis
import schedule
import time


r = redis.Redis(host="redis-12764.skr.demo.redislabs.com", port=12764)


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


def fetch_data_from_json(file_path='/Users/shekharsuman/customers/indigo/pocpython/DEl-BOM-27-28-29.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to find and cache minimum fare in Redis
def cache_minimum_fare():
    data = fetch_data_from_json()

    if data:
        min_fare = extract_min_fare(data)
        

        # Cache minimum fare in a sorted set in Redis
        for member, score in min_fare.items():
            r.zadd('DEL-BOM', {member: score})

        print(f"Minimum fare {min_fare} cached in Redis at {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Schedule the job to run every 5 minutes
# schedule.every(5).minutes.do(cache_minimum_fare)
cache_minimum_fare()
# Run the scheduled job indefinitely
# while True:
#     schedule.run_pending()
#     time.sleep(1)
