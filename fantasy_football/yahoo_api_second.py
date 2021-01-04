from requests import get, post
import json
import webbrowser
import base64


client_id = 'dj0yJmk9VEswVEhQWjd4ZE9YJmQ9WVdrOVEydEJVSFpvTkRrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PWZk'
client_secret = '5cac93055b55b321450a43a02047f7e7bee9a14b'
base_url = 'https://api.login.yahoo.com/'

code_url = f'oauth2/request_auth?client_id={client_id}&redirect_uri=oob&response_type=code&language=en-us'
webbrowser.open(base_url + code_url)

code = 'pqvvhqn'

encoded = base64.b64encode((client_id + ':' + client_secret).encode("utf-8"))
headers = {
    'Authorization': f'Basic {encoded.decode("utf-8")}',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'grant_type': 'authorization_code',
    'redirect_uri': 'oob',
    'code': code
}

response = post(base_url + 'oauth2/get_token', headers=headers, data=data)
response.ok
response.json()
access_token = response.json()['access_token']
refresh_token = response.json()['refresh_token']

# For refreshing the access token
data = {
    'grant_type': 'refresh_token',
    'redirect_uri': 'oob',
    'code': code,
    'refresh_token': refresh_token
}
response = post(base_url + 'oauth2/get_token', headers=headers, data=data)
access_token = response.json()['access_token']


# Testing the access token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
response = get('https://api.gemini.yahoo.com/v3/rest/advertiser/', headers=headers)
response.json()['response']



