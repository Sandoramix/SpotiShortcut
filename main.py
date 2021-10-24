import os
import threading
from time import sleep
from pynput import keyboard
import Spotify_custom as s


pause=False




def press(key):
    global pause
    # FULLY CUSTOMIZABLE SHORCUTS
    # "Key" : [action,parameter]
    # "Key" : [action,None] -> without any parameters
    shorcuts={
        "f9":[close,None],

        "f7":[spotify.remove_current_from_playlist,'0XEZPioQQwZfuiTpVAGNlp'],
        "f8":[spotify.add_current_to_playlist,'0XEZPioQQwZfuiTpVAGNlp'],
                                                #MY PLAYLISTS :)
        "\\":[spotify.remove_current_from_playlist,'1OlRxahyVfzqjLtJltXmlZ'],
        "]":[spotify.add_current_to_playlist,'1OlRxahyVfzqjLtJltXmlZ'],

        "+":[spotify.add_current_to_liked,None],
        "-":[spotify.remove_current_from_liked,None],

        #don't change 'pause'
        "pause":"f5"
    }

    try:
        k = key.char 
    except:
        k = key.name
    if k==shorcuts["pause"]: 
        pause=not pause
        if not pause:
            print(f"RESUMED\n{spotify.line2}")
    if pause and (k in list(shorcuts.keys()) or k==shorcuts["pause"]):
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
    sleep(2)
    exit()  

def listener():
    with keyboard.Listener(on_press=press) as listener:
        listener.join()
th1=threading.Thread(target=listener,name="LISTENER").start()

spotify=s.Spotify_custom()
