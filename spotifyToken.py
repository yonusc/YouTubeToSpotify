import base64
import requests

client_id = 'c809b977677b45bcb6eb07936cd699be'
client_secret = '616baaf2d66b430f95564bc3e08fc746'

# Concatenate client_id and client_secret
client_credentials = f"{client_id}:{client_secret}"

# Encode the string in base64
encoded_credentials = base64.b64encode(client_credentials.encode('utf-8')).decode('utf-8')

# Defines token URL and headers for the request
token_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Define the body of POST request
body = {
    'grant_type' : 'client_credentials'
}

# Make POST request to access token
response = requests.post(token_url, headers=headers, data=body)

# Check if the request was successful
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']
    print(f"Access Token: {access_token}")
else:
    print(f"Failed to retrieve access token: {response.status_code}")
    print(response.text)

