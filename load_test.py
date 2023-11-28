from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Simulate a user waiting between 1 and 3 seconds between tasks

    @task
    def my_api_request(self):
        # Define the API endpoint you want to test
        endpoint = "/getFlightData"
        query_params = {"date": "2023-11-27", "s": "DEL", "d":"BOM"}

        
        # Make a request to your API
        response = self.client.get(endpoint,params=query_params)

        # You can add assertions or other processing here if needed
        # Example: assert response.status_code == 200

# Run Locust with the following command in your terminal
# locust -f load_test.py --host=http://your-api-host
