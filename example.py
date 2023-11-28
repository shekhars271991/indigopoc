import redis
import json


data = {
    'dog': {
        'scientific-name' : 'Canis familiaris'
    }
}

r = redis.Redis(host="redis-12764.skr.demo.redislabs.com", port=12764)

try:
    # If data is not in cache, fetch the JSON file (simulate API call)
    with open('/Users/shekharsuman/customers/indigo/pocpython/navitaire_default.json', 'r') as file:
        sample_data = json.load(file)

    # Store the fetched data in Redis cache
    r.json().set("test1", "$", sample_data)

    
except Exception as e:
    print(f"Error fetching and caching data: {e}")


r.json().set('doc', '$', data)



# doc = r.json().get('doc', '$')
# dog = r.json().get('doc', '$.dog')
# scientific_name = r.json().get('doc', '$..scientific-name')
