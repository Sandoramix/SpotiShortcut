# SpotiShortcut
- Needs Python3
- Add/Delete the song you're listening to with a simple shorcut


- It uses spotipy & sqlite3 for local storage

# Dependencies:
- spotipy
- requests
- pynput

# Installation:
* Go to [Spotify Developers Dashboard](https://developer.spotify.com/dashboard/) and create an application
* In app Settings set "Redirect url" to http://127.0.0.1:9005
* Edit .env_example
* Run init.bat

# Current avaiable actions
* add_current_to_playlist       = Add currently listening song to a specific playlist
* remove_current_from_playlist  = Try to remove currently listening song from a specific playlist
* add_current_to_liked          = Add currently listening song to liked
* remove_current_from_liked     = Try to remove currently listening song from liked
* loop_toggle                   = Change loop state (as in Spotify application)
* shuffle_toggle                = Change shuffle state (as in Spotify application)
