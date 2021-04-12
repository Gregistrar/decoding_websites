import pandas as pd
from requests import get, post
import json
import webbrowser
import base64

client_id = 'dj0yJmk9VEswVEhQWjd4ZE9YJmQ9WVdrOVEydEJVSFpvTkRrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PWZk'
client_secret = '5cac93055b55b321450a43a02047f7e7bee9a14b'
base_url = 'https://api.login.yahoo.com/'


code_url = f'oauth2/request_auth?client_id={client_id}&redirect_uri=oob&response_type=code&language=en-us'
webbrowser.open(base_url + code_url)
print(base_url + code_url)

code = 'ccnnjxs'

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
response.json()

access_token = response.json()['access_token']
refresh_token = response.json()['refresh_token']


# Refresh access token
data = {
    'grant_type': 'refresh_token',
    'redirect_uri': 'oob',
    'code': code,
    'refresh_token': refresh_token
}
response = post(base_url + 'oauth2/get_token', headers=headers, data=data)
access_token = response.json()['access_token']



















if __name__ == "__main__":
    league_id = '338380'  # put your real league id here
    game_id = "370"  # put the game id here (game id's reflect the type of sport and the year)
    game_code = "nfl"  # put the game code here
    season = "2020"  # put the year of the current fantasy season
    auth_dir = 'C:/Users/ghodg/Desktop'  # put the location where you are storing the client_id/secret
    working_dir = 'C:/Users/ghodg/Desktop/'  # put the location where you want excel file to be saved
    excel_file_name = 'Points.xlsx'  # Name your file after you set up the headers

    team_list_today = pull_data(season, league_id, game_id, game_code, auth_dir)
    write_to_sheet(working_dir, excel_file_name, team_list_today)






