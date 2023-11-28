from flask import Flask, request, jsonify
import redis
import json
import time 

app = Flask(__name__)

# Create a Redis client
r = redis.Redis(host="redis-12764.skr.demo.redislabs.com", port=12764)
# r.json().set("DEL:BOM", "$", {})


# Endpoint to get flight data
# http://127.0.0.1:3000/getFlightData?date=2023-11-27&s=DEL&d=BOM
@app.route('/getFlightData', methods=['GET'])
def get_flight_data():


    dateparam = request.args.get('date')
    source = request.args.get('s')    
    dest = request.args.get('d') 


    # Check if data is in Redis cache
    key = source + ":" + dest + ":" + dateparam

    cached_data = r.get(key)

    if cached_data:
        # If data is cached, return it to the client
        return jsonify(json.loads(cached_data))

    try:
        # If data is not in cache, fetch the JSON file (simulate API call)
        #generate file name
        filename = source+"-"+dest+"_"+dateparam+".json"
        with open('/Users/shekharsuman/customers/indigo/pocpython/'+filename, 'r') as file:
            flight_data = json.dumps(json.load(file))

        time.sleep(3)
        r.setex(key, 60, flight_data) # set an expire in 60 secs
        return jsonify(flight_data)
    except Exception as e:
        print(f"Error fetching and caching data: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(port=3000)
