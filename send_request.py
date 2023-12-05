import requests

base_url = 'http://127.0.0.1:8080'

# Send request to /start endpoint
start_response = requests.get(f'{base_url}/start')
if start_response.status_code == 200:
    print('Request to /start successful')
else:
    print('Request to /start failed')

# # Send request to /show endpoint
# show_response = requests.get(f'{base_url}/show')
# if show_response.status_code == 200:
#     print('Request to /show successful')
#     print('Response content:')
#     print(show_response.text)  # Print the response content
# else:
#     print('Request to /show failed')

