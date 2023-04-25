import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from PIL import Image
from io import BytesIO
import spotipy.util as util
import sys


scope = "user-read-playback-state"
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# cur_track = sp.current_playback()
# duration = cur_track['item']["duration_ms"] // 1000
# progress = cur_track['progress_ms'] //1000
# name = cur_track['item']['name']
# artist = cur_track['item']['artists'][0]['name']
# shuffle = cur_track['shuffle_state']
# repeat_state = cur_track['repeat_state']

# perc = int(round((progress/duration) * 100))

# mins, secs = divmod((duration-progress), 60)
# print("-{:0>2}:{:0>2}".format(mins, secs))

# mins, secs = divmod(progress, 60000)
# print("{:0>2}:{:0>2}".format(mins, secs))

# print(perc)
# print(name)
# print(artist)
# print(type(shuffle))
# print(repeat_state + '.png')
# response = requests.get(cur_track['item']['album']['images'][0]['url'])
# image = Image.open(BytesIO(response.content))
# image.thumbnail((30, 30), Image.LANCZOS)
# image.show()
