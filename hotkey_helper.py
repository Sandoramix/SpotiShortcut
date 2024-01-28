import os
from pynput import keyboard as pyk
from app.utils import forgeHotkey, formatKey, isSpecialKey

# The currently pressed keys
CURRENT=set()


LISTENER: pyk.Listener=None



def onPress(key: "(pyk.Key | pyk.KeyCode | None)"):
	if LISTENER==None or key==None: return
	CURRENT.add(key)

	if key == pyk.Key.esc and LISTENER:
		LISTENER.stop()



def onRelease(key: "(pyk.Key | pyk.KeyCode | None)"):
	if LISTENER==None or key==None: return
	global CURRENT
	currentKeys=list(CURRENT)
	currentKeys.sort(key=lambda x: chr(0) if isSpecialKey(x) else formatKey(x,LISTENER.canonical(x)))

	if key in CURRENT:
		CURRENT=set()

	strKeys:list[str]=[
		formatKey(k,LISTENER.canonical(k))
		for k in currentKeys
		if formatKey(k,LISTENER.canonical(k)) != None
	]

	if len(strKeys)==0: return
	finalHotkey=forgeHotkey(strKeys)

	print()
	print(finalHotkey)





def main():
	"""helper that is used to find which string of key combinations to insert in the configuration file
	"""
	global LISTENER
	LISTENER=pyk.Listener(on_press=onPress, on_release=onRelease)
	try:
		LISTENER.start()
		LISTENER.join()
	except KeyboardInterrupt:
		exit(1)

if __name__=="__main__":
	print("Press any hotkey/s to get the string \nor ESC to stop the program.\nP.s. do not exaggerate :)")
	main()