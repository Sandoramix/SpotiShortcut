
import os
import datetime
import threading

import requests
import spotipy as spoti
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

import multiprocessing as multi

class Spoti():

    def __init__(self) -> None:
        self.line = "-"*50+"\n"

        self.API = os.environ['API']
        self.ID = os.environ['CLIENT_ID']
        self.SECRET = os.environ['CLIENT_SECRET']
        self.RED_URL = os.environ['RED_URL']
        self.SCOPES = os.environ['SCOPES']
        self.RTOKEN = os.environ['REFRESH_TOKEN']

        

        self.oauth = SpotifyOAuth(client_id=self.ID, client_secret=self.SECRET, redirect_uri=self.RED_URL, scope=self.SCOPES)
        self.session = Spotify(auth_manager=self.oauth)

        self.TOKEN = self.oauth.get_access_token(as_dict=False)
        
        self.tkn_update(True)
    
    


    def items_in_saved_check(self, songs=[]):
        try:
            return list(requests.get('https://api.spotify.com/v1/me/tracks/contains?ids='+','.join(songs), headers={'Authorization': f'Bearer {self.TOKEN}'}).json())
        except:
            return [False for i in songs]
    def current_song(self):
        return self.session.current_playback()

    def current_song_id(self) -> str:
        try:
            return self.current_song()['item']['id']
        except:
            print('NO SONG IS PLAYING')

    def song_name(self, song=None) -> str:
        if song == None:
            song = self.current_song()['item']
        elif isinstance(song, str):
            song = self.session.track(song)
        artists = ''
        for i in song['artists']:
            artists += i['name']+", "
        artists = artists[:len(artists)-2]

        return song['name'] + ' - ' + artists

    def song_ids_from_playlist(self, playlist='0c0dqQKnUr2O6nENHG3Lez'):
        raw = self.session.playlist(
            playlist_id=playlist, fields='tracks.items(track(id))')
        ids = []
        for i in raw['tracks']['items']:
            ids.append(i['track']['id'])

        return ids

    def remove_items_from_liked(self, songs=[]):
        check = self.items_in_saved_check(songs)
        for i in range(len(songs)):
            if check[i] == True:
                self.session.current_user_saved_tracks_delete([songs[i]])
                print("L[True] del - "+self.song_name(songs[i]))
            else:
                print("L[False] del - "+self.song_name(songs[i]))

    def add_items_to_liked(self, songs=[]):
        check = self.items_in_saved_check(songs)

        for i in range(len(songs)):
            if check[i] == False:
                self.session.current_user_saved_tracks_add([songs[i]])

                print("L[True] add - "+self.song_name(songs[i]))
            else:
                print("L[False] add - "+self.song_name(songs[i]))

    def remove_current_from_liked(self):
        self.remove_items_from_liked(songs=[self.current_song_id()])

    def add_current_to_liked(self):
        self.add_items_to_liked(songs=[self.current_song_id()])

    def add_items_to_playlist(self, songs, playlist='0c0dqQKnUr2O6nENHG3Lez'):
        pl_songs = self.song_ids_from_playlist(playlist=playlist)
        for i in songs:
            if i not in pl_songs:
                self.session.playlist_add_items(playlist, songs)
                print("P[True] add -"+self.song_name(i))
            else:
                print("P[False] add - "+self.song_name(i))

    def remove_items_from_playlist(self, songs=[], playlist='0c0dqQKnUr2O6nENHG3Lez'):
        pl_songs = self.song_ids_from_playlist(playlist=playlist)
        for i in songs:
            if i in pl_songs:
                self.session.playlist_remove_all_occurrences_of_items(
                    playlist, songs)
                print("P[True] del - "+self.song_name(i))
            else:
                print("P[False] del - "+self.song_name(i))

    def add_current_to_playlist(self, playlist='0c0dqQKnUr2O6nENHG3Lez'):
        self.add_items_to_playlist(
            songs=[self.current_song_id()], playlist=playlist)

    def remove_current_from_playlist(self, playlist='0c0dqQKnUr2O6nENHG3Lez'):
        self.remove_items_from_playlist(
            songs=[self.current_song_id()], playlist=playlist)




    
    def tkn_update(self,flag=False):
        self.th=threading.Timer(3600, self.tkn_update).start()
        #self.th.setName("TIMER")
        #self.th.start()

        if flag:
            print(f'{self.line}SPOTIFY LIST UPDATER {datetime.datetime.now()}\n{self.line}', end='')
            return

        print(f'{self.line}TOKEN UPDATED {datetime.datetime.now()}\n{self.line}', end='')
        self.oauth.refresh_access_token(self.RTOKEN)
        self.TOKEN = self.oauth.get_access_token(as_dict=False)

    def exit(self):
        try:
            self.th.cancel()
        except:
            pass
        SystemExit()