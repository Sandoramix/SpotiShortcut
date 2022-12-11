import os
from pynput import keyboard
from app.utils import forgeHotkey, formatKey, isSpecialKey

# The currently pressed keys
CURRENT=set()


LISTENER: keyboard.Listener=None



def on_press(key: (keyboard.Key | keyboard.KeyCode | None)):
	if LISTENER==None or key==None: return
	CURRENT.add(key)

	if key == keyboard.Key.esc and LISTENER:
		LISTENER.stop()


def on_release(key: (keyboard.Key | keyboard.KeyCode | None)):
	if LISTENER==None or key==None: return
	global CURRENT
	

	currentKeys=list(CURRENT)
	currentKeys.sort(key=lambda x: chr(0) if isSpecialKey(x) else formatKey(x,LISTENER.canonical(x)))

	if key in CURRENT:
		CURRENT=set()

	strKeys:list[str]=[]
	for k in currentKeys:
		_formatted=formatKey(k,LISTENER.canonical(k))
		if _formatted!=None:
			strKeys.append(_formatted)


	if len(strKeys)==0: return
	finalHotkey=forgeHotkey(strKeys)

	print()
	print(finalHotkey)

	
	




def main():
	"""Easy way to find out the keyboard name
	"""
	global LISTENER
	LISTENER=keyboard.Listener(on_press=on_press, on_release=on_release)
	try:
		LISTENER.start()
		LISTENER.join()
	except KeyboardInterrupt:
		exit(1)
	
if __name__=="__main__":
	print("Press any hotkey/s to get the string \nor ESC to stop the program.\nP.s. do not exaggerate :)")
	main()