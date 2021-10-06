import os
import threading
from pynput import keyboard
import Spotify as s


spotify=s.Spoti()



def press(key):
    try:
        k = key.char 
    except:
        k = key.name
    if k =="f7":
        spotify.remove_current_from_playlist(playlist='0XEZPioQQwZfuiTpVAGNlp')
    elif k == '+':
        spotify.add_current_to_liked()
    elif k == '-':
        spotify.remove_current_from_liked()
    elif k=='f8':
        spotify.add_current_to_playlist(playlist='0XEZPioQQwZfuiTpVAGNlp')
    elif k =='f9':
        exit()





def listener():
    with keyboard.Listener(on_press=press) as listener:
        listener.join()
threading.Thread(target=listener).start()
try:
    os.popen("C:\\Users\\sando\\AppData\\Roaming\\Spotify\\Spotify.exe")
except:
    pass