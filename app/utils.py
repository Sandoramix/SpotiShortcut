import os,yaml
import pynput.keyboard as pyk
import re

API="https://api.spotify.com/v1/"
SCOPES="user-follow-read user-top-read user-read-recently-played user-read-playback-position user-library-read user-library-modify user-read-currently-playing user-modify-playback-state user-read-playback-state user-read-email playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private"


# CONFIG.YAML UTILS
ADD_TO_PLAYLIST="addToPlaylist"
REM_FR_PLAYLIST="removeFromPlaylist"
ADD_TO_LIKED="addToLiked"
REM_FR_LIKED="removeFromLiked"
UPD_SHORTCUTS="updateShortcuts"
TGL_LOOP="toggleLoop"
TGL_SHUFFLE="toggleShuffle"
PAUSE="pause"
CLOSE="close"

CONFIG_TEMPLATE=f"""
# TEMPLATE
{ADD_TO_PLAYLIST}:
  key: playlist_id
  
  # if you want a hotkey with multiple keys, use this syntax
  <key>+<key>: playlist_id

{REM_FR_PLAYLIST}:
  key: playlist_id
  key: playlist_id

{ADD_TO_LIKED}: key
{REM_FR_LIKED}: key

{TGL_LOOP}: key
{TGL_SHUFFLE}: key

{UPD_SHORTCUTS}: key
{PAUSE}: key
{CLOSE}: key
"""

def loadConfig(abs_path):
	if not os.path.exists(abs_path): createConfig(abs_path)
	with open(abs_path,'r') as file:
		return yaml.safe_load(file)


def createConfig(path):
	with open(path,'w') as file:
		file.write(CONFIG_TEMPLATE)






# PYNPUT UTILS

def forgeHotkey(keys:(str|list[str]))->str:
	keys_list:list[str]=keys if type(keys) is list else [keys]
	
	if len(keys_list)==1:
		return keys_list[0]
	return '<'+'>+<'.join(keys_list)+'>'

def getHotkey(string:str)->list[str]:
	trimmed=string.replace(' ','')
	regex=re.compile(r'<(.*?)>\+?')
	
	if '>+<' not in trimmed: return [trimmed]
	
	return regex.findall(trimmed)


def sortedHotkey(hotkey:str):
	new_hotkey=getHotkey(hotkey)
	new_hotkey.sort()
	return forgeHotkey(new_hotkey)


def isSpecialKey(key):
	return hasattr(key,'_name_')

def formatKey(key,canonical_key):
	return key._name_ if isSpecialKey(key) else pynputKeyValue(canonical_key)



def pynputKeyValue(key:pyk.Key | pyk.KeyCode):
	if key==None: return None
	result=key._name_ if isSpecialKey(key) else key.char if hasattr(key,'char') else key.name if hasattr(key,'name') else key
	if result ==None: return None
	return str(result)

# OTHER
def line(ch="─", length=50) -> str:
		return ch*length