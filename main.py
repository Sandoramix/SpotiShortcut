import os
from pynput import keyboard
import threading
from time import sleep
import app.Spotify_custom as s
from app.utils import *


CONFIG_PATH=os.path.abspath("./config.yaml")

CONFIG=loadConfig(CONFIG_PATH)


from dotenv import load_dotenv
load_dotenv()

pause = False
SPOTIFY = s.Spotify_custom()


SHORTCUTS={}

def populateShortcuts(name,command,multiple=False):
	global SHORTCUTS
	if not name in CONFIG: return None
	data = CONFIG[name]
	if not data: return None
	if multiple and (type(data) is not dict): return None
	if not multiple and (type(data) is not str): return None

	if not multiple:
		SHORTCUTS[data]=[command,None]
		return
	

	for key,value in data.items():
		if not value or type(value) is not str: continue
		SHORTCUTS[key]=[command,value]
	

def updateShortcuts():
	global SHORTCUTS
	SHORTCUTS={}
	populateShortcuts(ADD_TO_PLAYLIST,SPOTIFY.add_current_to_playlist,True)
	populateShortcuts(REM_FR_PLAYLIST,SPOTIFY.remove_current_from_playlist,True)
	
	populateShortcuts(ADD_TO_LIKED,SPOTIFY.add_current_to_liked)
	populateShortcuts(REM_FR_LIKED,SPOTIFY.remove_current_from_liked)
	
	populateShortcuts(TGL_LOOP,SPOTIFY.loop_toggle)
	populateShortcuts(TGL_SHUFFLE,SPOTIFY.shuffle_toggle)
	populateShortcuts(PAUSE,None)

	populateShortcuts(UPD_SHORTCUTS,updateShortcuts)
	
	print(f"UPDATED SHORTCUTS\n{line()}")

	
updateShortcuts()

def press(key):
	global pause
	if not SHORTCUTS:
		updateShortcuts()


	k = key.char if hasattr(key,'char') else key.name if hasattr(key,'name') else key
	
	if k == SHORTCUTS['pause']:
			pause = not pause
			if not pause:
					print(f"RESUMED\n{line()}")

	if pause and (k in list(SHORTCUTS.keys()) or k == SHORTCUTS[PAUSE]):
			print(f"PAUSED [{SHORTCUTS['pause']} for resume]\n{line()}")
			return
	if pause:
			return

	if k not in SHORTCUTS:
			return

	if SHORTCUTS[k][1]:
			SHORTCUTS[k][0](SHORTCUTS[k][1])
	else:
			SHORTCUTS[k][0]()


def close():
	print(f"BYE!\n{SPOTIFY.line()}")
	SPOTIFY.exit()
	sleep(2)
	exit()




def listener():
	with keyboard.Listener(on_press=press) as listener:
			listener.join()


th1 = threading.Thread(target=listener, name="LISTENER").start()
