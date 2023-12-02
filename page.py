import requests

def send_show_request():
    # Data to be sent as query parameters
    data = {
        "key1": "value3",
        "key2": "value4"
    }

    # URL of the /show endpoint
    show_url = 'http://127.0.0.1:8080/show'

    # Sending the GET request with data as query parameters
    response = requests.get(show_url, params=data)

    # Checking the response status and content
    if response.status_code == 200:
        print("Show request successful!")
        print("Show Response:", response.json())
    else:
        print("Show request failed with status code:", response.status_code)

def send_start_request():
    # URL of the /start endpoint
    start_url = 'http://127.0.0.1:8080/start'

    # Sending the POST request to /start
    start_response = requests.post(start_url)

    # Checking the response status
    if start_response.status_code == 200:
        print("Start request successful! Variable changed.")
    else:
        print("Start request failed with status code:", start_response.status_code)


send_show_request()


# send_start_request()
