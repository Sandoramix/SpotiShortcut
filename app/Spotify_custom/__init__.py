
import os
import datetime
import threading
from app.utils import line,SCOPES,API

from spotipy import Spotify
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth


from app.Spotify_custom.database import SpotifyDB


class Spotify_custom():

    def __init__(self) -> None:

        self.th = [None]

        self.ID = os.environ['CLIENT_ID']
        self.SECRET = os.environ['CLIENT_SECRET']
        self.REDIRECT_URL = os.environ['REDIRECT_URL']
        

        self.oauth = SpotifyOAuth(
            client_id=self.ID, client_secret=self.SECRET, redirect_uri=self.REDIRECT_URL, scope=SCOPES)
        self.session = Spotify(oauth_manager=self.oauth)
        
        self.RTOKEN = self.oauth.get_access_token()["refresh_token"]

        self.TOKEN = self.oauth.get_access_token(as_dict=False)
        self.tkn_update(True)

        self.db = SpotifyDB(self.session)


    def current_playback(self, section=None) -> dict or None:
        raw = self.session.current_playback()
        if not raw:
            print(f'EXECUTION ERROR, TRY AGAIN\n{line()}')
            return None
        return raw if not section else raw[section]

    def loop_toggle(self) -> None:
        state = self.current_playback("repeat_state")

        if not state:
            return

        changed_state = "off"
        if state == "off":
            changed_state = "context"
        elif state == "context":
            changed_state = "track"

        self.session.repeat(changed_state)
        state = changed_state.upper()
        print(f'STATE CHANGED TO {state}\n{line()}')

    def shuffle_toggle(self) -> None:
        state = self.current_playback("shuffle_state")
        if not state:
            return

        self.session.shuffle(not state)
        print(f'SHUFFLE => {"ON" if not state else "OFF"}\n{line()}')

# ─────────────────────────────────────────────────────────────────────────────────────────────

    def likedSongsHandler(self, songs=[], removing=False) -> None:
        check = self.items_in_saved_check(songs)
        for i in range(len(songs)):
            result = False
            if check[i] == removing:
                if removing:
                    self.session.current_user_saved_tracks_delete([songs[i]])
                else:
                    self.session.current_user_saved_tracks_add([songs[i]])
                result = True
            print(f"[{'TRUE' if result else 'FALSE'}] SONG {'ADDED TO' if not removing else 'REMOVED FROM'} LIKED:\n=> {self.song_name(songs[i])}\n{line()}")

    def playlistSongsHandler(self, playlist, songs=[], removing=False) -> None:
        
        for i in songs:
            songExistInPlaylist = self.db.playlist_has_song(playlist, i)
            result = False

            song = self.db.song(i)
            if not song:
                song = self.db.json_extract_song_info(self.session.track(i))
            
            
            try:
                PLAYLIST=self.session.playlist(playlist)
                if not PLAYLIST: raise SpotifyException(-1,404,"Playlist doesn't exist")
                if removing and songExistInPlaylist:
                    self.session.playlist_remove_all_occurrences_of_items(playlist, songs)
                    self.db.playlist_delete_song(playlist, song[0])
                    result = True

                elif not removing and not songExistInPlaylist:
                    self.session.playlist_add_items(playlist, songs)
                    self.db.playlist_add_song(playlist, song)
                    result = True
            except KeyboardInterrupt:
                self.exit()
            
            except SpotifyException:
                print(f"[ERROR] INVALID PLAYLIST ID\n{line()}")
                continue
            except Exception as e:
                print(e)
            print(f"[{'TRUE' if result else 'FALSE'}] SONG {'REMOVED FROM' if removing else 'ADDED TO'} PLAYLIST {'['+PLAYLIST['name']+']' if 'name' in PLAYLIST else None}\n=> {self.song_name(song)}\n{line()}")
# ---------------------------------------------------------------------------------------------


# ─────────────────────────────────────────────────────────────────────────────────────────────

    def remove_current_from_liked(self) -> None:
        current = self.current_song_id()
        if current == None:
            return
        self.likedSongsHandler([current], True)

    def add_current_to_liked(self) -> None:
        current = self.current_song_id()
        if current == None:
            return
        self.likedSongsHandler([current])


# ---------------------------------------------------------------------------------------------

    def add_current_to_playlist(self, playlist) -> None:
        current = self.current_song_id()
        if current == None:
            return
        self.playlistSongsHandler(playlist, [current])

    def remove_current_from_playlist(self, playlist) -> None:
        current = self.current_song_id()
        if current == None:
            return
        self.playlistSongsHandler(playlist, [current], True)
# ─────────────────────────────────────────────────────────────────────────────────────────────

    def items_in_saved_check(self, songs=[]) -> list:
        if len(songs) == 0:
            return None
        return self.session.current_user_saved_tracks_contains(songs)

    def song_ids_from_playlist(self, playlist) -> list:
        ids = []
        tracks = self.db.playlist_json(playlist)['tracks']

        for i in tracks:
            ids.append(i[0])

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
            print(f'NO SONG IS PLAYING\n{line()}')
            return None
        return raw[0]

    def song_name(self, song=None, local=False) -> str:
        if song == None:
            song = self.db.json_extract_song_info(self.current_song())
        elif isinstance(song, str):
            song = self.db.json_extract_song_info(self.session.track(song))
        return song[1] + ' [' + song[2]+']'


# ───────────────────────────────────UpdateToken─────────────────────────────────────────────


    def tkn_update(self, flag=False) -> None:
        self.th[0] = threading.Timer(3600, self.tkn_update)
        self.th[0].start()

        if flag:
            print(
                f'{line()}\nSPOTIFY UPDATER │ {str(datetime.datetime.now()).replace(" "," │ ")}\n{line()}')
            return

        print(
            f'TOKEN UPDATED │ {str(datetime.datetime.now()).replace(" "," │ ")}\n{line()}')

        self.oauth.refresh_access_token(self.RTOKEN)
        self.TOKEN = self.oauth.get_access_token(as_dict=False)

# ─────────────────────────────────────Exit──────────────────────────────────────────────────
    def exit(self):
        try:
            self.th[0].cancel()
        except:
            print(f"ERROR WITH CLOSING THE TIMER THREAD\n{line()}")
        SystemExit()
