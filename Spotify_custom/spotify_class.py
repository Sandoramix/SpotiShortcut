
import os
import datetime
import threading

import json
from typing import Tuple
import requests
import spotipy as spoti
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import sqlite3

class Spotify_custom():

    def __init__(self) -> None:
        self.line = "-"*50
        self.line2="─"*50
        self.th=[None]
        #------------------------------------------------        
        self.API = os.environ['API']
        self.ID = os.environ['CLIENT_ID']
        self.SECRET = os.environ['CLIENT_SECRET']
        self.RED_URL = os.environ['RED_URL']
        self.SCOPES = os.environ['SCOPES']
        #------------------------------------------------
        self.oauth = SpotifyOAuth(client_id=self.ID, client_secret=self.SECRET, redirect_uri=self.RED_URL, scope=self.SCOPES)
        self.session = Spotify(oauth_manager=self.oauth)
        self.RTOKEN = self.oauth.get_access_token()["refresh_token"]
        #------------------------------------------------
        self.username=self.session.current_user()["id"]
        self.TOKEN = self.oauth.get_access_token(as_dict=False)
        self.tkn_update(True)
        
        self.dbInitialize()
        self.dbUpdateDB()

         
#─────────────────────────────────────────────────────────────────────────────────────────────
    def remove_items_from_liked(self, songs=[]):
        check = self.items_in_saved_check(songs)
        for i in range(len(songs)):
            if check[i] == True:
                self.session.current_user_saved_tracks_delete([songs[i]])
                print(f"[TRUE] DELETE\nLiked => {self.song_name(songs[i])}\n{self.line}")
            else:
                print(f"[FALSE] DELETE\nLiked => {self.song_name(songs[i])}\n{self.line}")

    def add_items_to_liked(self, songs=[]):
        check = self.items_in_saved_check(songs)

        for i in range(len(songs)):
            if check[i] == False:
                self.session.current_user_saved_tracks_add([songs[i]])
                print(f"[TRUE] ADD\nLiked => {self.song_name(songs[i])}\n{self.line}")
            else:
                print(f"[FALSE] ADD\nLiked => {self.song_name(songs[i])}\n{self.line}")

#---------------------------------------------------------------------------------------------
    def add_items_to_playlist(self,playlist, songs=[]):
        pl_songs = self.dbGetSongsIdsFromPlaylist(playlist)
        
        for i in songs:
            if i not in pl_songs:
                self.session.playlist_add_items(playlist, songs)

                song=self.jsonExtractSongInfo(self.session.track(i))

                self.dbAddSongs(song)
                print(f"[TRUE] ADD\nPlaylist => {song[1]} ─ {song[2]}\n{self.line}")
            else:
                song=self.dbGetSong(i)
                print(f"[FALSE] ADD\nPlaylist => {song[1]} ─ {song[2]}\n{self.line}")

    def remove_items_from_playlist(self,playlist, songs=[]):
        pl_songs = self.dbGetSongsIdsFromPlaylist(playlist)
        for i in songs:
            if i in pl_songs:
                self.session.playlist_remove_all_occurrences_of_items(playlist, songs)
                song=self.jsonExtractSongInfo(self.session.track(i))

                print(f"[TRUE] DELETE\nPlaylist => {song[1]} ─ {song[2]}\n{self.line}")
            else:
                song=self.dbGetSong(i)
                print(f"[FALSE] DELETE\nPlaylist => {song[1]} ─ {song[2]}\n{self.line}")  
#─────────────────────────────────────────────────────────────────────────────────────────────
    def remove_current_from_liked(self):
        current=self.current_song_id()
        if current==None:
            return
        self.remove_items_from_liked(songs=[current])

    def add_current_to_liked(self):
        current=self.current_song_id()
        if current==None:
            return
        self.add_items_to_liked(songs=[current])

#---------------------------------------------------------------------------------------------
    def add_current_to_playlist(self, playlist):
        current=self.current_song_id()
        if current==None:
            return
        self.add_items_to_playlist(songs=[current], playlist=playlist)

    def remove_current_from_playlist(self, playlist):
        current=self.current_song_id()
        if current==None:
            return
        self.remove_items_from_playlist(songs=[current], playlist=playlist)
#─────────────────────────────────────────────────────────────────────────────────────────────
    def items_in_saved_check(self, songs=[]):
        try:
            return list(requests.get('https://api.spotify.com/v1/me/tracks/contains?ids='+','.join(songs), headers={'Authorization': f'Bearer {self.TOKEN}'}).json())
        except:
            return [False for i in songs]

    def song_ids_from_playlist(self, playlist):
        raw = self.session.playlist(playlist_id=playlist, fields='tracks.items(track(id))')
        ids = []
        for i in raw['tracks']['items']:
            ids.append(i['track']['id'])

        return ids
#─────────────────────────────────────────────────────────────────────────────────────────────
    def current_song(self):
        raw=self.session.current_playback()
        if not raw:
            return None
        return self.jsonExtractSongInfo(self.session.current_playback()["item"])

    def current_song_id(self) -> str:
        try:
            return self.current_song()[0]
        except:
            print('NO SONG IS PLAYING')
            return None

    def song_name(self, song=None) -> str:
        if song == None:
            song = self.jsonExtractSongInfo(self.current_song())
        elif isinstance(song, str):
            song = self.jsonExtractSongInfo(self.session.track(song))
        return song[1] + ' - ' + song[2]
    def getUserPlaylists(self):
        return self.session.current_user_playlists()

#───────────────────────────────────UpdateToken─────────────────────────────────────────────
    def tkn_update(self,flag=False):
        self.th[0]=threading.Timer(3600, self.tkn_update)
        self.th[0].start()

        if flag:
            print(f'{self.line2}\nSPOTIFY UPDATER │ {str(datetime.datetime.now()).replace(" "," │ ")}\n{self.line2}')
            return

        print(f'TOKEN UPDATED │ {str(datetime.datetime.now()).replace(" "," │ ")}\n{self.line2}')

        self.oauth.refresh_access_token(self.RTOKEN)
        self.TOKEN = self.oauth.get_access_token(as_dict=False)














#─────────────────────────────────────────────────────────────────────────────────────────────
    def jsonExtractSongInfo(self,song) -> Tuple:
        s_id=song["id"]
        s_name=song["name"]
        s_duration=song["duration_ms"]
        s_pop=song["popularity"]
        s_artists=", ".join([i["name"] for i in song["artists"]])
        return (s_id,s_name,s_artists,s_duration,s_pop)
#────────────────────────────────────DATABASE─────────────────────────────────────────────────
#-------------------------------------GetData----------------------------------------------
    def dbGetSong(self,id):
        if self.dbHasSong(id):
            return self.dbExecute("select * from song where song_id='"+id+"'").fetchone()
        return None

    def dbGetPlaylists(self):
        return [i[0] for i in self.dbExecute("select playlist_id from playlist").fetchall()]

    def dbGetSongsIdsFromPlaylist(self,id_playlist):
        if not self.dbHasPlaylist(id_playlist):
            return []
        return [i[1] for i in self.dbExecute("select * from playlist_songs where playlist='"+id_playlist+"'",fetch=0)]
#-------------------------------------AddData-------------------------------------------------
    def dbAddSongs(self,song):
        if len(song)==0:
            return
        if not self.dbHasSong(song[0][0]):
            self.dbExecute("insert into song (song_id,name,artists,duration_ms,popularity) values(?,?,?,?,?)",song)
            
    def dbAddPlaylist(self,id,name,owner):
        if not self.dbHasPlaylist(id):
            self.dbExecute("insert into playlist(playlist_id,name,owner) values(?, ?, ?)",params=[(id,name,owner)])
#-------------------------------------UpdateData----------------------------------------------
    def dbUpdateFromPlaylists(self,pl_id):
        final_obj=self.session.playlist(pl_id)

        pl_name=final_obj["name"]
        pl_owner=final_obj["owner"]["id"]
        self.dbAddPlaylist(pl_id,pl_name,pl_owner)


        offs=100
        total=int(final_obj["tracks"]["total"])

        final_obj=final_obj["tracks"]["items"]

        while offs<=total:
            tmp=self.session.playlist_tracks(pl_id,limit=100,offset=offs,market=None)
            final_obj+=tmp["items"]
            offs+=100
        
        playlist_songs=[]

        new_songs=[]
        new_playlist_songs=[]
        for song in final_obj:
            song=song["track"]

            out=self.jsonExtractSongInfo(song)

            s_id=out[0]
            if not self.dbHasX(table="playlist_songs",name1="song",id1=s_id,name2="playlist",id2=pl_id):
                new_playlist_songs.append((pl_id,s_id))

            if not self.dbHasSong(s_id):
                new_songs.append(out)

            playlist_songs.append((pl_id,s_id))
        
        self.dbUpdatePlaylistSongs(new_playlist_songs)
        self.dbAddSongs(new_songs)

        self.dbRemoveDeletedPlaylistTracks(playlist_songs)


    def dbUpdatePlaylistSongs(self,array):
        self.dbExecute("insert into playlist_songs(playlist,song) values(?, ?)",array)
#-------------------------------------ClearData-----------------------------------------------
    def dbRemoveDeletedPlaylistTracks(self,songs):
        if len(songs)==0:
            return
        playlist_id=songs[0][0]
        
        db_songs=self.dbGetSongsIdsFromPlaylist(playlist_id)
        tmp_songs=[i[1] for i in songs]
        for x_song in db_songs:
            if x_song not in tmp_songs:
                self.dbExecute("delete from playlist_songs where playlist='"+playlist_id+"' and song='"+x_song+"'")


    def dbClearPlaylist(self,pl_id):
        self.dbExecute("delete from playlist_songs where playlist='"+pl_id+"'")

    def dbclearOldPlaylists(self,us_pl):
        db_pl=self.dbGetPlaylists()

        for pl in db_pl:
            if pl not in us_pl:
                self.dbClearPlaylist(pl)
                self.dbExecute("delete from playlist where playlist_id='"+pl+"'")
#-------------------------------------Utils--------------------------------------------------
    def dbHasPlaylist(self,id):
        if not self.dbHasX(table="playlist",name1="playlist_id",id1=id):
            return False
        return True

    def dbHasSong(self,id):
        if not self.dbHasX(table="song",name1="song_id",id1=id):
            return False
        return True
    
    def dbHasX(self,table,name1,id1,name2=None,id2=None):
        if not name2 or not id2:
            if not self.dbExecute("select * from "+table+" where "+name1+"='"+id1+"'").fetchone():
                return False
        else:
            if not self.dbExecute("select * from "+table+" where "+name1+"='"+id1+"' and "+name2+"='"+id2+"'").fetchone():
                return False
        return True

    def dbExecute(self,cmd,params=None,fetch=None):
        if params==None:
            data=self.db.execute(cmd)
        else:
            data=self.db.executemany(cmd,params)

        if "select" not in cmd:
            self.dbCommit()
        if fetch==None:
            return data
        if fetch==0:
            return data.fetchall()
        else:
            return data.fetchmany(fetch)

    def dbClose(self):
        self.db.close()

    def dbCommit(self):
        self.database.commit()
#-------------------------------------Main--------------------------------------------------- 

    def dbInitialize(self):
        if not os.path.exists("Spotify_custom/spotify.db"):
            self.database=sqlite3.connect("Spotify_custom/spotify.db")
            self.db=self.database.cursor()
            self.dbExecute("CREATE TABLE playlist (playlist_id STRING PRIMARY KEY, name STRING, owner STRING)")
            self.dbExecute("CREATE TABLE song (song_id STRING PRIMARY KEY UNIQUE, name STRING, artists STRING, duration_ms INTEGER, popularity INTEGER)")
            self.dbExecute("CREATE TABLE playlist_songs (playlist STRING REFERENCES playlist (playlist_id), song STRING REFERENCES song (song_id))")
            return
        self.database=sqlite3.connect("Spotify_custom/spotify.db",check_same_thread=False)
        self.db=self.database.cursor()

    def dbUpdateDB(self):
        print(f'UPDATING DATABASE...')
        us_playlist=[]
        raw=self.getUserPlaylists()
        for playlist in raw["items"]:
            if playlist["owner"]["id"]==self.username:
                self.dbUpdateFromPlaylists(playlist["id"])
                us_playlist.append(playlist["id"])
        self.dbclearOldPlaylists(us_pl=us_playlist)
        print(f'\nDATABASE UPDATED\n{self.line2}')
#─────────────────────────────────────Exit──────────────────────────────────────────────────
    def exit(self):
        try:
            self.th[0].cancel()
        except:
            print("ERROR WITH CLOSING THE TIMER THREAD")
        SystemExit()

