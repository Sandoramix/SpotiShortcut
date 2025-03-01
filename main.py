
from venv import logger
from pynput import keyboard as pyk
from pynput.keyboard import Key
import signal

import time
from app.custom_spotify import CustomSpotify
from app.utils import *

from dotenv import load_dotenv
import logging

#logging.basicConfig(filename='debug.log', level=logging.INFO)
# ----------------------------
load_dotenv()

def updateConfig():
	global CONFIG
	CONFIG=loadConfig("./config.yaml")

def close():
	print(f"BYE!\n{line()}")
	os.kill(os.getpid(), signal.SIGKILL)
# ----------------------------







def populateShortcuts(name,command,multiple=False):
	global SHORTCUTS

	if not name in CONFIG: return None
	hotkeys: ("dict[str,str] | str") = CONFIG[name]

	if not hotkeys: return None
	if multiple and (type(hotkeys) is not dict): return None
	if not multiple and (type(hotkeys) is not str and type(hotkeys) is not int): return None

	parsedKey = sortedHotkey(str(hotkeys).lower())


	if not multiple:
		if parsedKey not in SHORTCUTS:
			SHORTCUTS[parsedKey] = []
		SHORTCUTS[parsedKey].append([command,None])
		return


	for hotkey,value in hotkeys.items():
		parsedHotkey = sortedHotkey(str(hotkey).lower())
		if parsedHotkey not in SHORTCUTS:
			SHORTCUTS[parsedHotkey] = []
		if not value or type(value) is not str:
			print(f'INVALID VALUE ON [{parsedHotkey}] HOTKEY')
			continue
		SHORTCUTS[parsedHotkey].append([command,value])


def updateShortcuts():
	global SHORTCUTS
	updateConfig()
	SHORTCUTS={}

	populateShortcuts(ADD_TO_LIKED,SPOTIFY.add_current_to_liked)

	populateShortcuts(REM_FR_LIKED,SPOTIFY.remove_current_from_liked)

	populateShortcuts(ADD_TO_PLAYLIST,SPOTIFY.add_current_to_playlist,True)
	populateShortcuts(REM_FR_PLAYLIST,SPOTIFY.remove_current_from_playlist,True)



	populateShortcuts(TGL_LOOP,SPOTIFY.loop_toggle)
	populateShortcuts(TGL_SHUFFLE,SPOTIFY.shuffle_toggle)

	populateShortcuts(CLOSE,close)
	populateShortcuts(PAUSE,None)

	populateShortcuts(UPD_SHORTCUTS,updateShortcuts)

	print(f"SHORTCUTS UPDATED\n{line()}")




def onPress(_key):
	global PAUSED_STATUS
	try:
		if not SHORTCUTS:
			updateShortcuts()

		canonicalKey=_key if isSpecialKey(_key) else LISTENER.canonical(_key)
		#logger.info(f"{canonicalKey=}\t{'+'.join([str(i) for i in list(PRESSED_KEYS)])}")
		if any(modifier in PRESSED_KEYS for modifier in [Key.shift, Key.ctrl, Key.alt]):
			PRESSED_KEYS.add(_key)
		else:
			PRESSED_KEYS.add(canonicalKey)
	except:
		pass


def onRelease(_key):
	global PRESSED_KEYS
	global PAUSED_STATUS

	try:

		strKeys:list[str]=[
			formatKey(hkey,LISTENER.canonical(hkey))
			for hkey in list(PRESSED_KEYS)
			if formatKey(hkey,LISTENER.canonical(hkey))!=None
		]
		canonicalKey=_key if isSpecialKey(_key) else LISTENER.canonical(_key)

		if _key in PRESSED_KEYS: PRESSED_KEYS.remove(_key)
		if canonicalKey in PRESSED_KEYS: PRESSED_KEYS.remove(canonicalKey)
		if len(strKeys)==0: return
		hotkey=sortedHotkey(forgeHotkey(strKeys))
		PRESSED_KEYS = set()

		if  PAUSE in CONFIG and hotkey == CONFIG[PAUSE]:
				PAUSED_STATUS = not PAUSED_STATUS
				if not PAUSED_STATUS:
						print(f"RESUMED\n{line()}")
				else:
					print(f"PAUSED -> press [{CONFIG[PAUSE]}] to resume\n{line()}")
				return

		if PAUSED_STATUS and hotkey in SHORTCUTS.keys():
			if PAUSE in CONFIG:
				print(f"PAUSED -> press [{CONFIG[PAUSE]}] to resume\n{line()}")
			return

		if PAUSED_STATUS:
				return

		if hotkey not in SHORTCUTS:
				return
		actions = SHORTCUTS[hotkey]
		for action in actions:
			if action[1]:
				action[0](action[1])
			else:
				action[0]()
	except:
		pass



if __name__=="__main__":
	CONFIG={}
	updateConfig()

	SPOTIFY = CustomSpotify()

	SHORTCUTS = {}

	updateShortcuts()
	PAUSED_STATUS = False

	PRESSED_KEYS : "set[(pyk.Key | pyk.KeyCode)]"=set()
	with pyk.Listener(on_press=onPress,on_release=onRelease) as LISTENER:
		try:
			LISTENER.join()
		except KeyboardInterrupt:
			close()