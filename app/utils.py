import os,yaml

API="https://api.spotify.com/v1/"
SCOPES="user-follow-read user-top-read user-read-recently-played user-read-playback-position user-library-read user-library-modify user-read-currently-playing user-modify-playback-state user-read-playback-state user-read-email playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private"

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
  key2: playlist2_id

{REM_FR_PLAYLIST}:
  key: playlist_id
  key2: playlist2_id

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


def line(ch="─", length=50) -> str:
		return ch*length
