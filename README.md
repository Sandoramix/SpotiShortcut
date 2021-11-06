# SpotiShortcut
**It is my personal project, where i wanted to use [spotify api & pynput & sqlite3] for a simple actions automization **

---

#### It is written in Python 3.9
---

# Installation:
* Go to [Spotify Developers Dashboard](https://developer.spotify.com/dashboard/) and create an application
* In app Settings set "Redirect url" to http://127.0.0.1:9005
* Configure .env_example and save it as .env
* Run init.bat
## Dependencies:
- spotipy
- ~~pipenv~~ -> dotenv
- pynput

------------
# Current available actions
* <b>add_current_to_playlist   </b>    : *Add currently listening song to a specific playlist*
* <b>remove_current_from_playlist </b> : *Try to remove currently listening song from a specific playlist*
* <b>add_current_to_liked         </b> : *Add currently listening song to liked*
* <b>remove_current_from_liked    </b> : *Try to remove currently listening song from liked*
* <b>loop_toggle                  </b> : *Change loop state (as in Spotify application)*
* <b>shuffle_toggle               </b> : *Change shuffle state (as in Spotify application)*


[editor]:(https://pandao.github.io/editor.md/en.html)
