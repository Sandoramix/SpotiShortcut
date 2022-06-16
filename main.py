import os
import threading
from time import sleep
import Spotify_custom as s

from dotenv import load_dotenv
load_dotenv()

pause = False

from pynput import keyboard
def press(key):
    global pause
    # FULLY CUSTOMIZABLE SHORCUTS
    # "Key" : [action,parameter( for example playlist id)]
    # "Key" : [action,None] -> without any parameters

    # Spotify available actions:[
    #   add_current_to_playlist , remove_current_from_playlist
    #   add_current_to_liked , remove_current_from_liked
    #   loop_toggle , shuffle_toggle
    # ]
    shorcuts = {
        "f9": [close, None],

        "f7": [spotify.remove_current_from_playlist, 'PLAYLIST_ID'],
        "f8": [spotify.add_current_to_playlist, 'PLAYLIST_ID'],
        # MY PLAYLISTS :)
        "\\": [spotify.remove_current_from_playlist, 'PLAYLIST_ID'],
        "]": [spotify.add_current_to_playlist, 'PLAYLIST_ID'],

        "+": [spotify.add_current_to_liked, None],
        "-": [spotify.remove_current_from_liked, None],
        "<": [spotify.loop_toggle, None],
        "M": [spotify.shuffle_toggle, None],
        # don't change 'pause'
        "pause": "f5"
    }

    try:
        k = key.char
    except:
        try:
            k = key.name
        except:
            k = key
    if k == shorcuts['pause']:
        pause = not pause
        if not pause:
            print(f"RESUMED\n{spotify.line2}")

    if pause and (k in list(shorcuts.keys()) or k == shorcuts['pause']):
        print(f"PAUSED [F5 for resume]\n{spotify.line2}")
        return

    if pause:
        return

    if k not in shorcuts:
        return

    if shorcuts[k][1]:
        shorcuts[k][0](shorcuts[k][1])
    else:
        shorcuts[k][0]()


def close():
    print(f"BYE!\n{spotify.line2}")
    spotify.exit()
    exit()


spotify = s.Spotify_custom()


def listener():
    with keyboard.Listener(on_press=press) as listener:
        listener.join()


th1 = threading.Thread(target=listener, name="LISTENER").start()
