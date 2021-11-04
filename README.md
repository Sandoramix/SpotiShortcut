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
* <h2><b>add_current_to_playlist   </b> </h2>   = Add currently listening song to a specific playlist
* <b>remove_current_from_playlist </b> = Try to remove currently listening song from a specific playlist
* <b>add_current_to_liked         </b> = Add currently listening song to liked
* <b>remove_current_from_liked    </b> = Try to remove currently listening song from liked
* <b>loop_toggle                  </b> = Change loop state (as in Spotify application)
* <b>shuffle_toggle               </b> = Change shuffle state (as in Spotify application)
