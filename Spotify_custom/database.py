import os
import sqlite3
from typing import Tuple

from requests.api import delete


class SpotifyDB():
    def __init__(self, spotify_session) -> None:
        """Initialize database
        spotify_session= spotipy.Spotify() object
        """
        self.line = "-"*50
        self.line2 = "─"*50
        self.initialize()

        self.session = spotify_session
        self.username = self.session.current_user()["id"]

        self.updateDB()

    def initialize(self) -> None:
        if not os.path.exists("Spotify_custom/spotify.db"):
            self.database = sqlite3.connect(
                "Spotify_custom/spotify.db", check_same_thread=False)
            self.db = self.database.cursor()
            self.exec(
                "CREATE TABLE playlist (playlist_id STRING PRIMARY KEY, name STRING, owner STRING)")
            self.exec(
                "CREATE TABLE song (song_id STRING PRIMARY KEY UNIQUE, name STRING, artists STRING, duration_ms INTEGER, popularity INTEGER)")
            self.exec(
                "CREATE TABLE playlist_songs (playlist STRING REFERENCES playlist (playlist_id), song STRING REFERENCES song (song_id))")
            return
        self.database = sqlite3.connect(
            "Spotify_custom/spotify.db", check_same_thread=False)
        self.db = self.database.cursor()

# ─────────────────────────────────────────────────────────────────────────────────────────────

    def updateDB(self) -> None:
        print(f'UPDATING DATABASE - please wait...')
        us_playlists = []
        raw = self.session.current_user_playlists()

        for playlist in raw["items"]:
            if playlist["owner"]["id"] == self.username:

                self.updatePlaylist(playlist["id"])
                us_playlists.append(playlist["id"])

        self.delete_old_playlists(us_playlists)
        print(f'\nDATABASE UPDATED\n{self.line2}')

# -------------------------------------GetData----------------------------------------------
    def song(self, id) -> tuple:
        if not self.has_song(id):
            return None
        return self.exec("select * from song where song_id='"+id+"'", fetch=1)

    def playlist_ids(self):
        return [i[0] for i in self.exec("select playlist_id from playlist", fetch=0)]

    def playlist_songs_ids(self, id_playlist):
        if not self.playlist_exists(id_playlist):
            return []
        return [i[1] for i in self.exec("select * from playlist_songs where playlist='"+id_playlist+"'", fetch=0)]


# -------------------------------------AddData-------------------------------------------------


    def add_song(self, song) -> None:
        if type(song) is tuple:
            song = [song]
        for s in song:
            if not self.has_song(s[0]):
                self.exec(
                    "insert into song (song_id,name,artists,duration_ms) values(?,?,?,?)", [s])

    def add_playlist(self, id, name, owner) -> None:
        if not self.playlist_exists(id):
            self.exec("insert into playlist(playlist_id,name,owner) values(?, ?, ?)", [
                      (id, name, owner)])

    def playlist_add_song(self, playlist, song) -> None:
        if type(song) is tuple:
            song = [song]
        self.add_song(song)
        for s in song:
            if not self.playlist_has_song(playlist, s[0]):
                self.exec("insert into playlist_songs (playlist,song) values(?,?)", [
                          (playlist, s[0])])

    def playlist_delete_song(self, playlist, song) -> None:
        if self.playlist_has_song(playlist, song):
            self.exec("delete from playlist_songs where playlist='" +
                      playlist+"' and song='"+song+"'")
# -------------------------------------UpdateData----------------------------------------------

    def updatePlaylist(self, id) -> None:
        playlist = self.playlist_json(id)

        self.add_playlist(id, playlist["name"], playlist["owner"])

        tracks = playlist["tracks"]

        new_songs = []
        new_playlist_songs = []
        all_ids = []

        for song in tracks:
            song_id = song[0]
            all_ids.append(song_id)

            if not self.database_has(table="playlist_songs", param1="song", value1=song_id, param2="playlist", value2=id):
                new_playlist_songs.append((id, song_id))

            if not self.has_song(song_id):
                new_songs.append(song)

        for dbsong in self.playlist_songs_ids(id):
            if dbsong not in all_ids:
                self.playlist_delete_song(id, dbsong)

        self.exec(
            "insert into playlist_songs(playlist,song) values(?, ?)", new_playlist_songs)
        self.add_song(new_songs)

# ------------------------------------------------------------------------------------
    def clear_all_playlist_songs(self, id) -> None:
        self.exec("delete from playlist_songs where playlist='"+id+"'")

    def delete_old_playlists(self, playlists) -> None:
        db_playlists = self.playlist_ids()

        for pl in db_playlists:
            if pl not in playlists:
                self.clear_all_playlist_songs(pl)
                self.exec("delete from playlist where playlist_id='"+pl+"'")
# -------------------------------------Utils--------------------------------------------------

    def playlist_json(self, id) -> dict:
        playlist = self.session.playlist(id)

        final = {
            "name": playlist["name"],
            "owner": playlist["owner"]["id"],
            "total": int(playlist["tracks"]["total"]),
            "tracks": []
        }
        offs = 100
        tracks = playlist["tracks"]["items"]
        while offs <= final["total"]:
            tmp = self.session.playlist_tracks(
                id, limit=100, offset=offs, market=None)
            tracks += tmp["items"]
            offs += 100
        for song in tracks:
            final["tracks"].append(self.json_extract_song_info(song["track"]))

        return final

    def json_extract_song_info(self, object) -> Tuple:
        """Extract from api request only useful for this program information\n
        object= [spotify 'track' object]
        """
        s_id = object["id"]
        s_name = object["name"]
        s_duration = object["duration_ms"]
        s_artists = ", ".join([i["name"] for i in object["artists"]])
        return (s_id, s_name, s_artists, s_duration)

    def playlist_has_song(self, playlist_id, song_id) -> bool:
        if not self.database_has(table="playlist_songs", param1="playlist", value1=playlist_id, param2="song", value2=song_id):
            return False
        return True

    def playlist_exists(self, id) -> bool:
        if not self.database_has(table="playlist", param1="playlist_id", value1=id):
            return False
        return True

    def has_song(self, id) -> bool:
        if not self.database_has(table="song", param1="song_id", value1=id):
            return False
        return True

    def database_has(self, table, param1, value1, param2=None, value2=None) -> bool:
        if not param2 or not value2:
            if not self.exec("select * from "+table+" where "+param1+"='"+value1+"'", fetch=1):
                return False
        else:
            if not self.exec("select * from "+table+" where "+param1+"='"+value1+"' and "+param2+"='"+value2+"'", fetch=1):
                return False
        return True

    def exec(self, command, params=None, fetch=None) -> None or tuple or list:
        if params == None:
            data = self.db.execute(command)
        else:
            data = self.db.executemany(command, params)

        if "select" not in command:
            self.commit()
        if fetch == None:
            return data
        if fetch == 0:
            return data.fetchall()
        elif fetch == 1:
            return data.fetchone()
        return data.fetchmany(fetch)

    def close(self):
        self.db.close()

    def commit(self):
        self.database.commit()
