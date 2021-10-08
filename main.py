import os
import threading
from pynput import keyboard
import Spotify as s






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
        print("ADDIO")
        spotify.exit()
        SystemExit()




def listener():
    with keyboard.Listener(on_press=press) as listener:
        listener.join()
th1=threading.Thread(target=listener,name="LISTENER").start()
spotify=s.Spoti()

#print(threading.enumerate())
# try:
#     pass
#     #os.popen("C:\\Users\\sando\\AppData\\Roaming\\Spotify\\Spotify.exe")
# except:
#     pass