import requests
import json

# URL of the Flask API endpoint
api_url = "http://127.0.0.1:7860/run/predict/"
# api_url = "http://127.0.0.1:8888/run/predict/"  # This version is for docker (port 8888)
#read chat_history.json
# Data to send to the API
data = {
    #plot a graph
    "data": ["import matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 10, 100)\ny = np.sin(x)\nplt.plot(x, y)"],
    "fn_index": 0
}
headers = {
    "Content-Type": "application/json"
}

# Perform the POST request
response = requests.post(api_url, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Failed to get response: {response.status_code}, {response.text}")
