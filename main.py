import os
import spotipy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import ast
import requests 
import pandas as pd
from analysis import favorite_genre

load_dotenv()
# load env



# spotify auth manging
def get_spotify_data():
    auth_manager = SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    track_ids = []
    artist_genress = []
    track_loudness = []

    history = sp.current_user_recently_played()
    #print(history["items"][0].keys())
    for details in history["items"]:

        # get the artist and the track name from spotify
        artist = sp.artist(details["track"]["artists"][0]["external_urls"]["spotify"])
        artist_genres = artist["genres"]
        track_id = details["track"]["id"]
        track_loudnes = sp.audio_analysis(track_id=track_id)["track"]["loudness"]

        track_ids.append(track_id)
        artist_genress.append(artist_genres)
        track_loudness.append(track_loudnes)

    df = pd.DataFrame({"track_id":track_ids,"artist_genres":artist_genress,"track_loudness":track_loudness})
    df.to_csv("output.csv",encoding="utf-8-sig")
    return df

if __name__ == "__main__":
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")
    redirect_uri = os.getenv("redirect_uri") 
    scope = ["user-top-read","user-read-recently-played"] 
    key = os.getenv("Api_key") 
    df = get_spotify_data()
    fav_genr = favorite_genre(df)
