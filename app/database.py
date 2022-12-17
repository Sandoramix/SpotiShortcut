import os,sqlite3
from app.utils import line
import time
# TODO REMOVE DEBUGGING PRINTS
class SpotifyDB():
    def __init__(self, spotify_session) -> None:
        """Initialize database
        spotify_session= spotipy.Spotify() object
        """
        # start=time.time()
        self.db_path=os.path.abspath('./spotify.db') 

        self.initialize()

        self.session = spotify_session
        self.username = self.session.current_user()["id"]

        # TODO IMPROVE DB UPDATING
        self.updateDB()
        # end=time.time()
        # print(f'res=> {(end-start)*10**3:.03f}')

    def initialize(self) -> None:
        if not os.path.exists(self.db_path):
            self.database = sqlite3.connect(self.db_path, check_same_thread=False)
            self.db = self.database.cursor()
            self.exec(
                "CREATE TABLE playlist (playlist_id STRING PRIMARY KEY, name STRING, owner STRING)")
            self.exec(
                "CREATE TABLE song (song_id STRING PRIMARY KEY UNIQUE, name STRING, artists STRING, duration_ms INTEGER, popularity INTEGER)")
            self.exec(
                "CREATE TABLE playlist_songs (playlist STRING REFERENCES playlist (playlist_id), song STRING REFERENCES song (song_id))")
            return
        self.database = sqlite3.connect(self.db_path, check_same_thread=False)
        # self.database.set_trace_callback(print)
        self.db = self.database.cursor()

# ─────────────────────────────────────────────────────────────────────────────────────────────

    def updateDB(self) -> None:
        print(f'UPDATING DATABASE - please wait...')
        userPlaylists = []
        raw = self.session.current_user_playlists()

        for playlist in raw["items"]:
            if playlist["owner"]["id"] == self.username:
                
                self.updatePlaylist(playlist["id"])
                userPlaylists.append(playlist["id"])
                

        self.delete_old_playlists(userPlaylists)
        print(f'\nDATABASE UPDATED\n{line()}')

# -------------------------------------GetData----------------------------------------------
    def song(self, id) -> (tuple or None):
        self.exec("select * from song where song_id='"+id+"'", fetch=1)

    def playlist_ids(self):
        return [i[0] for i in self.exec("select playlist_id from playlist", fetch=0)]

    def playlist_songs_ids(self, id_playlist):
        return [i[1] for i in self.exec("select * from playlist_songs where playlist='"+id_playlist+"'", fetch=0) if i!=None and len(i)>0]


# -------------------------------------AddData-------------------------------------------------


    def saveTrack(self, song) -> None:
        if type(song) is tuple:
            song = [song]

        self.exec('insert or ignore into song (song_id,name,artists,duration_ms) values '+','.join([
            f'("{self.strEscape(str(s[0]))}","{self.strEscape(str(s[1]))}","{self.strEscape(str(s[2]))}","{self.strEscape(str(s[3]))}")' 
            for s in song
        ]))

    def addSongsToPlaylist(self, playlist_id, tracks:(str|tuple[str])) -> None:
        if type(tracks) is tuple:
            tracks = [tracks]
        self.exec("insert or ignore into playlist_songs(playlist,song) values "+','.join([ 
            f'("{self.strEscape(playlist_id)}","{self.strEscape(str(id if type(id) is str else id[0]))}")' for id in tracks 
        ]))

    def playlist_delete_song(self, playlist, song) -> None:
        self.exec(f'delete from playlist_songs where playlist="{playlist}" and song="{song}"')

    def addPlaylist(self,playlist_id:str,name:str, owner:str,tracks:list[any]=[]):
        self.exec('insert or ignore into playlist(playlist_id,name,owner) values(?,?,?)',[(playlist_id,name,owner)])
        allSongsIds:list[str]=[song[0] for song in tracks]
        
        localPlaylistSongsIds:list[str]=[s[0] for s in self.exec(f'select song from playlist_songs where playlist="{self.strEscape(playlist_id)}"',fetch=0) if s!=None]
        

        diffTracks=[track for track in allSongsIds if track[0] not in localPlaylistSongsIds]
        if len(diffTracks) ==0:
            return

        diffIds=[s[0] for s in diffTracks]

        self.exec(f'delete from playlist_songs where playlist="{playlist_id}" and song not in ("'+'","'.join(allSongsIds)+'")')
        
        
        self.addSongsToPlaylist(playlist_id,diffIds)
        self.saveTrack(diffTracks)

# -------------------------------------UpdateData----------------------------------------------

    def updatePlaylist(self, playlist_id:str) -> None:
        playlist = self.playlist_json(playlist_id)

        self.addPlaylist(playlist_id, playlist["name"], playlist["owner"],playlist["tracks"])

# ------------------------------------------------------------------------------------
    def clear_all_playlist_songs(self, id) -> None:
        self.exec("delete from playlist_songs where playlist='"+id+"'")

    def delete_old_playlists(self, existingPlaylists:list[str]) -> None:
        query='delete from playlist where playlist_id not in ("'+'","'.join(existingPlaylists)+'")'
        self.exec(query)
        
        
# -------------------------------------Utils--------------------------------------------------
    def strEscape(self,string:str):
        return string.replace('"','""').replace("'","''")
    
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

    def json_extract_song_info(self, object) -> tuple:
        """Extract from api request only useful for this program information\n
        
        """
        s_id = object["id"]
        s_name = object["name"]
        s_duration = object["duration_ms"]
        s_artists = ", ".join([i["name"] for i in object["artists"]])
        return (s_id, s_name, s_artists, s_duration)

    def playlist_has_song(self, playlist_id, song_id) -> bool:
        return self.database_has(table="playlist_songs", param1="playlist", value1=playlist_id, param2="song", value2=song_id)

    def playlist_exists(self, id) -> bool:
        return self.database_has(table="playlist", param1="playlist_id", value1=id)

    def has_song(self, id) -> bool:
        return self.database_has(table="song", param1="song_id", value1=id)

    def database_has(self, table, param1, value1, param2=None, value2=None) -> bool:
        query=f'select * from {table} where {param1}="{value1}"' +f' and {param2}="{value2}"' if param2!=None and value2!=None else ""
        if not self.exec(query, fetch=1):
            return False
        
        return True

    def exec(self, command:str, params=None, fetch=None) -> None or tuple or list:
        if params == None:
            data = self.db.execute(command)
        else:
            data = self.db.executemany(command, params)

        if not command.lower().strip().startswith("select"):
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
