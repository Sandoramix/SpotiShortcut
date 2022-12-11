import os
from pynput import keyboard
from app.utils import formatKey, isSpecialKey

# The old/currently active modifiers
CURRENT=set()


LISTENER: keyboard.Listener=None



def on_press(key: (keyboard.Key | keyboard.KeyCode | None)):
	if LISTENER==None or key==None: return
	CURRENT.add(key)

	if key == keyboard.Key.esc and LISTENER:
		LISTENER.stop()


def on_release(key: (keyboard.Key | keyboard.KeyCode | None)):
	if LISTENER==None or key==None: return

	keyList=list(CURRENT)
	keyList.sort(key=lambda x: chr(0) if isSpecialKey(x) else formatKey(x,LISTENER.canonical(x)))

	if key in CURRENT:
		CURRENT.remove(key)

	formattedKeys:list[str]=[]
	for k in keyList:
		_formatted=formatKey(k,LISTENER.canonical(k))
		if _formatted!=None:
			formattedKeys.append(_formatted)


	length=len(formattedKeys)
	if length==0: return
	finalHotkeys=f'{formattedKeys[0]}' if length==1 else '<'+'>+<'.join(formattedKeys)+'>'

	print()
	print(finalHotkeys)

	
	




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