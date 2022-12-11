
from pynput import keyboard as pyk

import threading
from time import sleep
from app.custom_spotify import CustomSpotify
from app.utils import *

from dotenv import load_dotenv

# ----------------------------
load_dotenv()

def updateConfig():
	global CONFIG
	CONFIG=loadConfig("./config.yaml")

def close():
	print(f"BYE!\n{line()}")
	SPOTIFY.exit()
	if LISTENER: LISTENER.stop()
	sleep(2)
	exit(0)
# ----------------------------


CONFIG={}
updateConfig()

SPOTIFY = CustomSpotify()

SHORTCUTS = {}

PAUSED_STATUS = False

LISTENER:pyk.Listener=None
PRESSED_KEYS : set[(pyk.Key | pyk.KeyCode)]=set()




def populateShortcuts(name,command,multiple=False):
	global SHORTCUTS
	
	if not name in CONFIG: return None
	hotkeys: (dict[str,str] | str) = CONFIG[name]

	if not hotkeys: return None
	if multiple and (type(hotkeys) is not dict): return None
	if not multiple and (type(hotkeys) is not str): return None

	if not multiple:
		SHORTCUTS[forgeHotkey(sortedHotkey(hotkeys.lower()))]=[command,None]
		return
	

	for hotkey,value in hotkeys.items():
		if not value or type(value) is not str: continue
		SHORTCUTS[forgeHotkey(sortedHotkey(hotkey.lower()))]=[command,value]
	

def updateShortcuts():
	global SHORTCUTS
	updateConfig()
	SHORTCUTS={}

	populateShortcuts(ADD_TO_PLAYLIST,SPOTIFY.add_current_to_playlist,True)
	populateShortcuts(REM_FR_PLAYLIST,SPOTIFY.remove_current_from_playlist,True)
	
	populateShortcuts(ADD_TO_LIKED,SPOTIFY.add_current_to_liked)
	populateShortcuts(REM_FR_LIKED,SPOTIFY.remove_current_from_liked)
	
	populateShortcuts(TGL_LOOP,SPOTIFY.loop_toggle)
	populateShortcuts(TGL_SHUFFLE,SPOTIFY.shuffle_toggle)
	
	populateShortcuts(CLOSE,close)
	populateShortcuts(PAUSE,None)

	populateShortcuts(UPD_SHORTCUTS,updateShortcuts)
	
	print(f"SHORTCUTS UPDATED\n{line()}")

	
updateShortcuts()



def onPress(_key):
	global PAUSED_STATUS
	if not SHORTCUTS:
		updateShortcuts()

	PRESSED_KEYS.add(_key)



	strKeys:list[str]=[ 
		formatKey(hkey,LISTENER.canonical(hkey)) 
		for hkey in list(PRESSED_KEYS) 
		if formatKey(hkey,LISTENER.canonical(hkey))!=None 
	]

	if len(strKeys)==0: return
	hotkey=forgeHotkey(strKeys)

	if hotkey == CONFIG[PAUSE]:
			PAUSED_STATUS = not PAUSED_STATUS
			if not PAUSED_STATUS:
					print(f"RESUMED\n{line()}")
			else:
				print(f"PAUSED -> press [{CONFIG[PAUSE]}] to resume\n{line()}")
			return

	if PAUSED_STATUS and hotkey in SHORTCUTS.keys():
			print(f"PAUSED -> press [{CONFIG[PAUSE]}] to resume\n{line()}")
			return

	if PAUSED_STATUS:
			return

	if hotkey not in SHORTCUTS:
			return

	if SHORTCUTS[hotkey][1]:
			SHORTCUTS[hotkey][0](SHORTCUTS[hotkey][1])
	else:
			SHORTCUTS[hotkey][0]()

def onRelease(_key):
	if _key in PRESSED_KEYS:  PRESSED_KEYS.remove(_key)



def listener():	
	global LISTENER
	LISTENER=pyk.Listener(on_press=onPress,on_release=onRelease)

	LISTENER.start()
	LISTENER.join()


if __name__=="__main__":
	th1 = threading.Thread(target=listener, name="LISTENER").start()	
