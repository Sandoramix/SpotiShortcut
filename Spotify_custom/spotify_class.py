
import os
import datetime
import threading

from typing import Dict, Tuple
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

 
 
 

from Spotify_custom.database import SpotifyDB


class Spotify_custom():

    def __init__(self) -> None:

        self.line2 = "─"*50
        self.th = [None]
        # ------------------------------------------------
        self.API = os.environ['API']
        self.ID = os.environ['CLIENT_ID']
        self.SECRET = os.environ['CLIENT_SECRET']
        self.RED_URL = os.environ['RED_URL']
        self.SCOPES = os.environ['SCOPES']
        # ------------------------------------------------
        self.oauth = SpotifyOAuth(
            client_id=self.ID, client_secret=self.SECRET, redirect_uri=self.RED_URL, scope=self.SCOPES)
        self.session = Spotify(oauth_manager=self.oauth)
        self.RTOKEN = self.oauth.get_access_token()["refresh_token"]
        # ------------------------------------------------

        self.TOKEN = self.oauth.get_access_token(as_dict=False)
        self.tkn_update(True)

        self.db = SpotifyDB(self.session)

# ─────────────────────────────────────────────────────────────────────────────────────────────
    def line(self, ch="-", length=50) -> str:
        return ch*length

    def current_playback(self) -> Dict or None:
        raw = self.session.current_playback()
        if not raw:
            msg = "EXECUTION ERROR, TRY AGAIN"
            print(f'{msg}\n{self.line(length=len(msg))}')
            return None
        return raw

    def loop_toggle(self) -> None:
        state = self.current_playback()
        msg = "STATE CHANGED TO "
        if not state:
            return
        state = state["repeat_state"]
        changed_state = "off"
        if state == "off":
            changed_state = "context"
        elif state == "context":
            changed_state = "track"

        self.session.repeat(changed_state)
        state = changed_state.upper()
        print(f'{msg}{state}\n{self.line(length=len(msg+state))}')

    def shuffle_toggle(self) -> None:
        state = self.current_playback()
        msg = "SHUFFLE "
        if not state:
            return

        state = state["shuffle_state"]
        changed_state = "ON"
        if state:
            changed_state = "OFF"
        self.session.shuffle(not state)
        print(f'{msg}{changed_state}\n{self.line(length=len(msg+changed_state))}')

# ─────────────────────────────────────────────────────────────────────────────────────────────

    def remove_items_from_liked(self, songs=[]) -> None:
        check = self.items_in_saved_check(songs)
        for i in range(len(songs)):
            if check[i] == True:
                self.session.current_user_saved_tracks_delete([songs[i]])

                print(
                    f"[TRUE] DELETE\nLiked => {self.song_name(songs[i])}\n{self.line()}")
            else:
                print(
                    f"[FALSE] DELETE\nLiked => {self.song_name(songs[i])}\n{self.line()}")

    def add_items_to_liked(self, songs=[]) -> None:
        check = self.items_in_saved_check(songs)

        for i in range(len(songs)):
            if check[i] == False:
                self.session.current_user_saved_tracks_add([songs[i]])
                print(
                    f"[TRUE] ADD\nLiked => {self.song_name(songs[i])}\n{self.line()}")
            else:
                print(
                    f"[FALSE] ADD\nLiked => {self.song_name(songs[i])}\n{self.line()}")

# ---------------------------------------------------------------------------------------------
    def add_items_to_playlist(self, playlist, songs=[]) -> None:
        for i in songs:
            if not self.db.playlist_has_song(playlist, i):
                self.session.playlist_add_items(playlist, songs)

                song = self.db.json_extract_song_info(self.session.track(i))

                self.db.playlist_add_song(playlist, song)
                print(
                    f"[TRUE] ADD\nPlaylist => {song[1]} ─ {song[2]}\n{self.line()}")
            else:
                song = self.db.song(i)
                print(
                    f"[FALSE] ADD\nPlaylist => {song[1]} ─ {song[2]}\n{self.line()}")

    def remove_items_from_playlist(self, playlist, songs=[]) -> None:
        for i in songs:
            if self.db.playlist_has_song(playlist, i):
                self.session.playlist_remove_all_occurrences_of_items(
                    playlist, songs)

                song = self.db.song(i)

                self.db.playlist_delete_song(playlist, song[0])

                print(
                    f"[TRUE] DELETE\nPlaylist => {song[1]} ─ {song[2]}\n{self.line()}")
            else:
                song = self.db.json_extract_song_info(self.session.track(i))

                print(
                    f"[FALSE] DELETE\nPlaylist => {song[1]} ─ {song[2]}\n{self.line()}")
# ─────────────────────────────────────────────────────────────────────────────────────────────

    def remove_current_from_liked(self) -> None:
        current = self.current_song_id()
        if current == None:
            return
        self.remove_items_from_liked(songs=[current])

    def add_current_to_liked(self) -> None:
        current = self.current_song_id()
        if current == None:
            return
        self.add_items_to_liked(songs=[current])

# ---------------------------------------------------------------------------------------------
    def add_current_to_playlist(self, playlist) -> None:
        current = self.current_song_id()
        if current == None:
            return
        self.add_items_to_playlist(songs=[current], playlist=playlist)

    def remove_current_from_playlist(self, playlist) -> None:
        current = self.current_song_id()
        if current == None:
            return
        self.remove_items_from_playlist(songs=[current], playlist=playlist)
# ─────────────────────────────────────────────────────────────────────────────────────────────

    def items_in_saved_check(self, songs=[]) -> list:
        try:
            return list(requests.get('https://api.spotify.com/v1/me/tracks/contains?ids='+','.join(songs), headers={'Authorization': f'Bearer {self.TOKEN}'}).json())
        except:
            return [False for i in songs]

    def song_ids_from_playlist(self, playlist) -> list:
        raw = self.session.playlist(
            playlist_id=playlist, fields='tracks.items(track(id))')
        ids = []
        for i in raw['tracks']['items']:
            ids.append(i['track']['id'])

        return ids
# ─────────────────────────────────────────────────────────────────────────────────────────────

    def current_song(self) -> dict:
        raw = self.session.current_playback()
        if not raw:
            return None
        return self.db.json_extract_song_info(self.session.current_playback()["item"])

    def current_song_id(self) -> str:
        raw = self.current_song()
        if raw == None:
            print('NO SONG IS PLAYING')
            return None
        return raw[0]

    def song_name(self, song=None) -> str:
        if song == None:
            song = self.db.json_extract_song_info(self.current_song())
        elif isinstance(song, str):
            song = self.db.json_extract_song_info(self.session.track(song))
        return song[1] + ' - ' + song[2]


# ───────────────────────────────────UpdateToken─────────────────────────────────────────────

    def tkn_update(self, flag=False) -> None:
        self.th[0] = threading.Timer(3600, self.tkn_update)
        self.th[0].start()

        if flag:
            print(
                f'{self.line2}\nSPOTIFY UPDATER │ {str(datetime.datetime.now()).replace(" "," │ ")}\n{self.line2}')
            return

        print(
            f'TOKEN UPDATED │ {str(datetime.datetime.now()).replace(" "," │ ")}\n{self.line2}')

        self.oauth.refresh_access_token(self.RTOKEN)
        self.TOKEN = self.oauth.get_access_token(as_dict=False)

# ─────────────────────────────────────Exit──────────────────────────────────────────────────
    def exit(self):
        try:
            self.th[0].cancel()
        except:
            print("ERROR WITH CLOSING THE TIMER THREAD")
        SystemExit()
