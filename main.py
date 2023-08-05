from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import time
import random
from app_gui import open_interface


load_dotenv()


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}







def get_playlist_id():
    #playlist_url = input("Enter playlist url: ")
    playlist_url = open_interface()
    playlist_id = playlist_url.split("/")[4]
    return playlist_id

def get_playlist_songs(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    print(type(json_result))
    return json_result


token = get_token()
playlist_id = get_playlist_id()
playlist_data = get_playlist_songs(token, playlist_id)

songs = playlist_data["items"]


#for i, song in enumerate(songs):
#    print(f"{i + 1}. {song['track']['name']} : {song['track']['external_urls']['spotify']}")



## discord messages part

webhook_url = os.getenv("WEBHOOK_URL")
authorization = dict(authorization = os.getenv("AUTHORIZATION"))
request_url = os.getenv("REQUEST_URL")

song_list = list()
for i,each_song in enumerate(songs):
    song_list.append(each_song['track']['name'])

random.shuffle(song_list)

i=0
for each_song in song_list:
    payload = dict(content = f"!play {each_song}")
    response = post(request_url, json = payload, headers = authorization)
    print(i)
    i+=1
    time.sleep(4)










