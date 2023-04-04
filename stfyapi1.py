import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import json

scope = "user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id='9945ba88f86e4bb6a0472eae6481a1f8',client_secret='eb1d0755d383480ba3e3c01f318e19da',redirect_uri="http://example.com"))
cur_track = sp.current_playback()
cur_album = cur_track['item']['album']['images'][0]['url']

print(cur_track)

with open("data_file.json", "r") as write_file:
    cache_album = json.load(write_file)

try:    
    if cur_album != cache_album:
        print("changing the album cover")
        with open("data_file.json", "w") as write_file:
            json.dump(cur_album, write_file) 
except:
    with open("data_file.json", "w") as write_file:
            json.dump(cur_album, write_file) 
                

# except spotipy.SpotifyStateError:
#     print("state error")

# except spotipy.SpotifyOauthError:
#     print("oauth error")

# except spotipy.SpotifyException:
#     print("error") 