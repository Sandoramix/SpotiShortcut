# SpotiShortcut

**With this app you can easily manage currently listening song with custom shortcuts**.
**It also uses a local sqlite database for songs caching**.

- Adding/removing it from playlist/liked
- Toggling the shuffle or loop button

---

## Installation

- Go to [Spotify Developers Dashboard](https://developer.spotify.com/dashboard/) and create an application

- In app Settings set "Redirect url" to <http://127.0.0.1:9005>
- Configure .env_example and save it as .env
- Run init.bat
- configure config_example.yaml and save it as config.yaml
  - _If you need help with key names, run hotkey_helper.bat
- Run generated start.bat

---

## Python 3.10

- pynput
- python-dotenv
- PyYAML
- requests
- spotipy
