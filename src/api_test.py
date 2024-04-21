import requests
import json

# URL of the Flask API endpoint
api_url = "http://127.0.0.1:7860/run/predict/"  # Adjust port if Flask is running on a different one
#read chat_history.json
chat_history = json.load(open("chat_history.json", "r"))
#append "test to chat_history to front"
# Data to send to the API
data = {
    "data": ["test",chat_history],
    "fn_index": 0
}
headers = {
    "Content-Type": "application/json"
}

# Perform the POST request
response = requests.post(api_url, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    # Process the successful response
    result = response.json()
    print(result)
else:
    # Handle errors
    print(f"Failed to get response: {response.status_code}, {response.text}")
