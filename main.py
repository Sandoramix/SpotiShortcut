from pynput import keyboard
import threading
from time import sleep
import Spotify_custom as s

from dotenv import load_dotenv
load_dotenv()

pause = False


def press(key):
    global pause
    #
    # FULLY CUSTOMIZABLE SHORCUTS
    # "Key" : [action,parameter] ->Used for [add_current_to_playlist,remove_current_from_playlist] commands
    # "Key" : [action,None] ->Used for [ add_current_to_liked,remove_current_from_liked,loop_toggle,shuffle_toggle] commands

    # Spotify available actions:[
    #   add_current_to_playlist , remove_current_from_playlist
    #   add_current_to_liked , remove_current_from_liked
    #   loop_toggle , shuffle_toggle
    # ]
    shorcuts = {
        "f10": [close, None],


        "f6": [spotify.remove_current_from_playlist, 'PLAYLIST'],
        "f7": [spotify.add_current_to_playlist, 'PLAYLIST'],
        "\\": [spotify.remove_current_from_playlist, 'PLAYLIST'],
        "]": [spotify.add_current_to_playlist, 'PLAYLIST'],
        ".": [spotify.remove_current_from_playlist, 'PLAYLIST'],
        "'": [spotify.add_current_to_playlist, 'PLAYLIST'],

        "f2": [spotify.add_current_to_liked, None],
        "f3": [spotify.remove_current_from_liked, None],
        # "<": [spotify.loop_toggle, None],
        # "M": [spotify.shuffle_toggle, None],
        # don't change 'pause'
        "pause": "f4"
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
            print(f"RESUMED\n{spotify.line()}")

    if pause and (k in list(shorcuts.keys()) or k == shorcuts['pause']):
        print(f"PAUSED [{shorcuts['pause']} for resume]\n{spotify.line()}")
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
    print(f"BYE!\n{spotify.line()}")
    spotify.exit()
    sleep(2)
    exit()


spotify = s.Spotify_custom()


def listener():
    with keyboard.Listener(on_press=press) as listener:
        listener.join()


th1 = threading.Thread(target=listener, name="LISTENER").start()
