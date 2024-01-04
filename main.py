import os
import spotipy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import json
import ast
import requests 

load_dotenv()
# load env
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = os.getenv("redirect_uri") 
scope = ["user-top-read","user-read-recently-played"] 
key = os.getenv("Api_key") 
api_key = os.getenv("lyrics_api")

def get_lyrics(track, artist, api_key):
    base_url = "https://api.musixmatch.com/ws/1.1/"
    method = "matcher.lyrics.get"
    params = {
        "format": "json",
        "callback": "callback",
        "q_track": track,
        "q_artist": artist,
        "apikey": api_key
    }
    response = requests.get(base_url + method, params=params)
    return response.json()

# Usage




# spotify auth manging
auth_manager = SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth_manager=auth_manager)
user = sp.current_user()
play_list = sp.user_playlists(user["id"],limit=10)
songs = sp.user_playlist(user=user["id"],playlist_id=play_list["items"][0]["id"])

user_music_history = {"items":[]}


history = sp.current_user_recently_played()
#print(history["items"][0].keys())
for details in history["items"]:

    # get the artist and the track name from spotify
    track_name = ast.literal_eval(f'"{details["track"]["name"]}"')
    artist_name = details["track"]["artists"][0]["name"]
    artist = sp.artist(details["track"]["artists"][0]["external_urls"]["spotify"])
    artist_genres = artist["genres"]
    track_id = details["track"]["id"]
    track_loudnes = sp.audio_analysis(track_id=track_id)["track"]["loudness"]

    try:
        api_call = get_lyrics(track_name, artist_name, api_key)
        lyrics = api_call["message"]["body"]["lyrics"]["lyrics_body"]
    except:
        lyrics = ""

    res = {
        "track_id" : track_id,
        "artist_name": artist_name,
        "track_name": track_name,
        "artist_genres": artist_genres,
        "song_lyrics" : lyrics,
        "track_loudness":track_loudnes
    }
    user_music_history["items"].append(res)

with open("output.json","w", encoding='utf-8') as f:
    json.dump(user_music_history,f,indent=4,ensure_ascii=False,)
