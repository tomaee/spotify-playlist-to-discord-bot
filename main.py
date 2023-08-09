from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import time
import random
from app_gui import open_interface


load_dotenv()


def token_variables_init():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    return url,headers,data

def playlist_variables_init(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": "Bearer " + token}
    return url,headers

def get_token():
    url, headers, data = token_variables_init() #necessary variables

    result = post(url, headers=headers, data=data) #sends request to spotify
    json_result = json.loads(result.content) #stores the result
    token = json_result["access_token"] #gets the token from the result
    return token

def get_playlist_id():
    #playlist_url = input("Enter playlist url: ")
    playlist_url = open_interface()
    playlist_id = playlist_url.split("/")[4]
    return playlist_id

def get_playlist_songs(token, playlist_id):
    url, headers = playlist_variables_init(token, playlist_id)

    result = get(url, headers=headers) #gets the data from spotify
    json_result = json.loads(result.content)["tracks"] #separates the songs
    #print(type(json_result))
    return json_result

def get_shuffled_songs(songs):
    song_list = list()
    for i,each_song in enumerate(songs):
        song_list.append(each_song['track']['name'])

    random.shuffle(song_list)
    return song_list

def get_songs_info():
    token = get_token()
    playlist_id = get_playlist_id()
    playlist_data = get_playlist_songs(token, playlist_id)
    songs = playlist_data["items"]
    return songs

## discord messages part

def discord_player(song_list):
    authorization, request_url = discord_variables_init()
    i=0
    for each_song in song_list:
        payload = dict(content = f"!play {each_song}")
        response = post(request_url, json = payload, headers = authorization)
        print(i)
        i+=1
        time.sleep(4)

def discord_variables_init():
    authorization = dict(authorization = os.getenv("AUTHORIZATION"))
    request_url = os.getenv("REQUEST_URL")
    return authorization,request_url

def main():
    songs = get_songs_info()
    song_list = get_shuffled_songs(songs)
    discord_player(song_list)




main()










