import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from pprint import pprint

date = input("Enter your desired date, it should follow this format YYYY-MM-DD: ")

url = "https://www.billboard.com/charts/hot-100/"
SPOTIPY_CLIENT_ID = 'YOUR SPOTIPY CLIENT ID'
SPOTIPY_CLIENT_SECRET = 'YOUR SPOTIPY CLIENT SECRET'
USERNAME = 'YOUR USERNAME' #Username ID, not the display name
OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Authenticating Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id = SPOTIPY_CLIENT_ID,
        client_secret = SPOTIPY_CLIENT_SECRET,
        redirect_uri= "http://example.com",
        scope = "playlist-modify-private",
        cache_path = "token.txt",
        username = USERNAME,
        show_dialog= True,
    )
)
# user_id = sp.current_user()["id"]
# print(user_id)

# Scraping Billboard 100
response = requests.get(f"{url}/{date}")
soup = BeautifulSoup(response.text,"html.parser")
songs = soup.select("li ul li h3")
songs_titles = [song.getText().strip() for song in songs]
# print(songs_titles)

# Searching for songs on Spotify
song_uris = []
year = date.split("-")[0]
for song in songs_titles:
    result = sp.search(q=f"track:{song} year:{year}", type = "track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
# pprint(song_uris)

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=USERNAME, name=f"{date} Billboard 100", public = False, description = "This is a playlist created by a Python script.")
# print(playlist)

#Addding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)