# turing-smart-screen-python - a Python system monitor and library for 3.5" USB-C displays like Turing Smart Screen or XuanFang
# https://github.com/mathoudebine/turing-smart-screen-python/

# Copyright (C) 2021-2023  Matthieu Houdebine (mathoudebine)
# Copyright (C) 2022-2023  Rollbacke
# Copyright (C) 2022-2023  Ebag333
# Copyright (C) 2022-2023  w1ld3r
# Copyright (C) 2022-2023  Charles Ferguson (gerph)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import locale
import json
import babel.dates
import platform

from PIL import Image
from io import BytesIO
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from psutil._common import bytes2human

import library.config as config
from library.display import display
from library.log import logger

CONFIG_DATA = config.CONFIG_DATA
ETH_CARD = CONFIG_DATA["config"]["ETH"]
WLO_CARD = CONFIG_DATA["config"]["WLO"]
HW_SENSORS = CONFIG_DATA["config"]["HW_SENSORS"]

try:
    scope = "user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id='9945ba88f86e4bb6a0472eae6481a1f8',client_secret='eb1d0755d383480ba3e3c01f318e19da',redirect_uri="http://example.com"))
    cur_track = sp.current_playback()
    with open("pback_cache.json", "w") as write_file:
        json.dump(cur_track, write_file)

except:
    with open("pback_cache.json", "w") as write_file:
        json.dump(None, write_file)

def get_full_path(path, name):
    if name:
        return path + name
    else:
        return None

class Cover:
    @staticmethod
    def cover_art():
        try:
            cur_track = sp.current_playback()
            cur_album = cur_track['item']['album']['images'][0]['url']
            with open("data.json", "r") as write_file:
                cache_track = json.load(write_file)

            try:
                if cur_album != cache_track:
                    with open("data_file.json", "w") as write_file:
                        json.dump(cur_album, write_file) 
                    response = requests.get(cur_album)
                    cover = Image.open(BytesIO(response.content))
            except:
                with open("data_file.json", "w") as write_file:
                    json.dump(cur_album, write_file) 
                    
        except:
            cover = Image.open(config.THEME_DATA['PATH'] + 'blank.png')

        cover.thumbnail((170, 170), Image.LANCZOS)
        if config.THEME_DATA['DIMAGE']['COVERART']['CURCOVER']['IMAGE'].get("SHOW", False):
            display.lcd.DisplayPILImage(
                image= cover,
                x=config.THEME_DATA['DIMAGE']['COVERART']['CURCOVER']['IMAGE'].get("X", 0),
                y=config.THEME_DATA['DIMAGE']['COVERART']['CURCOVER']['IMAGE'].get("Y", 0),
                )

class Device:
    @staticmethod
    def track_control():    
        try:
            cur_track = sp.current_playback()
            shuffle = str(cur_track['shuffle_state'])
            repeat_state = cur_track['repeat_state']
        except Exception as e:
            shuffle, repeat_state = 'False', 'off'

        if config.THEME_DATA['DIMAGE']['DEVICE']['SHUFFLE']['IMAGE'].get("SHOW", False):
            display.lcd.DisplayPILImage(
                image=Image.open(config.THEME_DATA['PATH'] + shuffle +'.png'),
                x=config.THEME_DATA['DIMAGE']['DEVICE']['SHUFFLE']['IMAGE'].get("X", 0),
                y=config.THEME_DATA['DIMAGE']['DEVICE']['SHUFFLE']['IMAGE'].get("Y", 0),
                image_width=config.THEME_DATA['DIMAGE']['DEVICE']['SHUFFLE']['IMAGE'].get("WIDTH", 0),
                image_height=config.THEME_DATA['DIMAGE']['DEVICE']['SHUFFLE']['IMAGE'].get("HEIGHT", 0)
            )

        if config.THEME_DATA['DIMAGE']['DEVICE']['REPEAT']['IMAGE'].get("SHOW", False):
            display.lcd.DisplayPILImage(
                image= Image.open(config.THEME_DATA['PATH'] + repeat_state + '.png'),
                x=config.THEME_DATA['DIMAGE']['DEVICE']['REPEAT']['IMAGE'].get("X", 0),
                y=config.THEME_DATA['DIMAGE']['DEVICE']['REPEAT']['IMAGE'].get("Y", 0),
                image_width=config.THEME_DATA['DIMAGE']['DEVICE']['REPEAT']['IMAGE'].get("WIDTH", 0),
                image_height=config.THEME_DATA['DIMAGE']['DEVICE']['REPEAT']['IMAGE'].get("HEIGHT", 0)
            )

class Track:
    @staticmethod
    def names():
        try:
            cur_track = sp.current_playback()
            name = cur_track['item']['name']
            artist = cur_track['item']['artists'][0]['name']
        except:
            name, artist = ' ', ' '

        if config.THEME_DATA['STATS']['TRACK']['TITLE']['TEXT'].get("SHOW", False):
            display.lcd.DisplayText(
                text = str((name[:21] + '...') if len(name) > 24 else (name + " " * (24-len(name)) if len(name) < 24 else name)),
                x=config.THEME_DATA['STATS']['TRACK']['TITLE']['TEXT'].get("X", 0),
                y=config.THEME_DATA['STATS']['TRACK']['TITLE']['TEXT'].get("Y", 0),
                font=config.THEME_DATA['STATS']['TRACK']['TITLE']['TEXT'].get("FONT", "roboto-mono/RobotoMono-Regular.ttf"),
                font_size=config.THEME_DATA['STATS']['TRACK']['TITLE']['TEXT'].get("FONT_SIZE", 10),
                font_color=config.THEME_DATA['STATS']['TRACK']['TITLE']['TEXT'].get("FONT_COLOR", (0, 0, 0)),
                background_color=config.THEME_DATA['STATS']['TRACK']['TITLE']['TEXT'].get("BACKGROUND_COLOR", (255, 255, 255)),
            )

        if config.THEME_DATA['STATS']['TRACK']['ARTIST']['TEXT'].get("SHOW", False):
            display.lcd.DisplayText(
                text = str((artist[:27] + '...') if len(artist) > 30 else (artist + ' ' * (30-len(artist)) if len(artist) < 30 else artist)),
                x=config.THEME_DATA['STATS']['TRACK']['ARTIST']['TEXT'].get("X", 0),
                y=config.THEME_DATA['STATS']['TRACK']['ARTIST']['TEXT'].get("Y", 0),
                font=config.THEME_DATA['STATS']['TRACK']['ARTIST']['TEXT'].get("FONT", "roboto-mono/RobotoMono-Regular.ttf"),
                font_size=config.THEME_DATA['STATS']['TRACK']['ARTIST']['TEXT'].get("FONT_SIZE", 10),
                font_color=config.THEME_DATA['STATS']['TRACK']['ARTIST']['TEXT'].get("FONT_COLOR", (0, 0, 0)),
                background_color=config.THEME_DATA['STATS']['TRACK']['ARTIST']['TEXT'].get("BACKGROUND_COLOR", (255, 255, 255)),
            )
    
    @staticmethod
    def progress():
        try:
            cur_track = sp.current_playback()
            duration = cur_track['item']["duration_ms"] //1000
            progress = cur_track['progress_ms'] //1000
            perc = int(round((progress/duration) * 100))

        except:
            duration, progress, perc = 0, 0, 0

        if config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("SHOW", False):
            display.lcd.DisplayProgressBar(
                x=config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("X", 0),
                y=config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("Y", 0),
                width=config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("WIDTH", 0),
                height=config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("HEIGHT", 0),
                value=perc,
                min_value=config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("MIN_VALUE", 0),
                max_value=config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("MAX_VALUE", 100),
                bar_color=config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("BAR_COLOR", (0, 0, 0)),
                bar_outline=config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("BAR_OUTLINE", False),
                background_color=config.THEME_DATA['STATS']['TRACK']['PLAYBACK']['GRAPH'].get("BACKGROUND_COLOR",
                                                                                       (255, 255, 255)),
            )

        if config.THEME_DATA['STATS']['TRACK']['PROGRESS']['TEXT'].get("SHOW", False):
            mins, secs = divmod(progress, 60)
            display.lcd.DisplayText(
                text = '{:0>2}:{:0>2}'.format(mins, secs),
                x=config.THEME_DATA['STATS']['TRACK']['PROGRESS']['TEXT'].get("X", 0),
                y=config.THEME_DATA['STATS']['TRACK']['PROGRESS']['TEXT'].get("Y", 0),
                font=config.THEME_DATA['STATS']['TRACK']['PROGRESS']['TEXT'].get("FONT", "roboto-mono/RobotoMono-Regular.ttf"),
                font_size=config.THEME_DATA['STATS']['TRACK']['PROGRESS']['TEXT'].get("FONT_SIZE", 10),
                font_color=config.THEME_DATA['STATS']['TRACK']['PROGRESS']['TEXT'].get("FONT_COLOR", (0, 0, 0)),
                background_color=config.THEME_DATA['STATS']['TRACK']['PROGRESS']['TEXT'].get("BACKGROUND_COLOR", (255, 255, 255)),                
            )
        
        if config.THEME_DATA['STATS']['TRACK']['REMAINDER']['TEXT'].get("SHOW", False):
            mins, secs = divmod((duration-progress), 60)
            display.lcd.DisplayText(
                text = '-{:0>2}:{:0>2}'.format(mins, secs),
                x=config.THEME_DATA['STATS']['TRACK']['REMAINDER']['TEXT'].get("X", 0),
                y=config.THEME_DATA['STATS']['TRACK']['REMAINDER']['TEXT'].get("Y", 0),
                font=config.THEME_DATA['STATS']['TRACK']['REMAINDER']['TEXT'].get("FONT", "roboto-mono/RobotoMono-Regular.ttf"),
                font_size=config.THEME_DATA['STATS']['TRACK']['REMAINDER']['TEXT'].get("FONT_SIZE", 10),
                font_color=config.THEME_DATA['STATS']['TRACK']['REMAINDER']['TEXT'].get("FONT_COLOR", (0, 0, 0)),
                background_color=config.THEME_DATA['STATS']['TRACK']['REMAINDER']['TEXT'].get("BACKGROUND_COLOR", (255, 255, 255)),
                )

class Date:
    @staticmethod
    def stats():
        date_now = datetime.datetime.now()

        if platform.system() == "Windows":
            # Windows does not have LC_TIME environment variable, use deprecated getdefaultlocale() that returns language code following RFC 1766
            lc_time = locale.getdefaultlocale()[0]
        else:
            lc_time = babel.dates.LC_TIME

        if config.THEME_DATA['STATS']['DATE']['DAY']['TEXT'].get("SHOW", False):
            date_format = config.THEME_DATA['STATS']['DATE']['DAY']['TEXT'].get("FORMAT", 'medium')
            display.lcd.DisplayText(
                text=f"{babel.dates.format_date(date_now, format=date_format, locale=lc_time)}",
                x=config.THEME_DATA['STATS']['DATE']['DAY']['TEXT'].get("X", 0),
                y=config.THEME_DATA['STATS']['DATE']['DAY']['TEXT'].get("Y", 0),
                font=config.THEME_DATA['STATS']['DATE']['DAY']['TEXT'].get("FONT",
                                                                           "roboto-mono/RobotoMono-Regular.ttf"),
                font_size=config.THEME_DATA['STATS']['DATE']['DAY']['TEXT'].get("FONT_SIZE", 10),
                font_color=config.THEME_DATA['STATS']['DATE']['DAY']['TEXT'].get("FONT_COLOR", (0, 0, 0)),
                background_color=config.THEME_DATA['STATS']['DATE']['DAY']['TEXT'].get("BACKGROUND_COLOR",
                                                                                       (255, 255, 255)),
                background_image=get_full_path(config.THEME_DATA['PATH'],
                                               config.THEME_DATA['STATS']['DATE']['DAY']['TEXT'].get("BACKGROUND_IMAGE",
                                                                                                     None))
            )

        if config.THEME_DATA['STATS']['DATE']['HOUR']['TEXT'].get("SHOW", False):
            time_format = config.THEME_DATA['STATS']['DATE']['HOUR']['TEXT'].get("FORMAT", 'medium')
            display.lcd.DisplayText(
                text=f"{babel.dates.format_time(date_now, format=time_format, locale=lc_time)}",
                x=config.THEME_DATA['STATS']['DATE']['HOUR']['TEXT'].get("X", 0),
                y=config.THEME_DATA['STATS']['DATE']['HOUR']['TEXT'].get("Y", 0),
                font=config.THEME_DATA['STATS']['DATE']['HOUR']['TEXT'].get("FONT",
                                                                            "roboto-mono/RobotoMono-Regular.ttf"),
                font_size=config.THEME_DATA['STATS']['DATE']['HOUR']['TEXT'].get("FONT_SIZE", 10),
                font_color=config.THEME_DATA['STATS']['DATE']['HOUR']['TEXT'].get("FONT_COLOR", (0, 0, 0)),
                background_color=config.THEME_DATA['STATS']['DATE']['HOUR']['TEXT'].get("BACKGROUND_COLOR",
                                                                                        (255, 255, 255)),
                background_image=get_full_path(config.THEME_DATA['PATH'],
                                               config.THEME_DATA['STATS']['DATE']['HOUR']['TEXT'].get(
                                                   "BACKGROUND_IMAGE",
                                                   None))
            )
