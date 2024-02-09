import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "6fecd06fa63f472b96ea3fda949c2c33"
CLIENT_SECRET = "a8bb11aafd584360aae81db383941adc"
USERNAME = "8e696bhuxmcylsjfi25cmwpnq"

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])