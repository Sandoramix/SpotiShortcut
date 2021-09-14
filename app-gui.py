from logging import debug, setLoggerClass
import subprocess

import datetime
import time

import requests as req
from pynput import keyboard

from requests.models import Response
from requests.sessions import session

#import spotify_token
import spotipy as spoti
from spotipy.oauth2 import SpotifyOAuth
import json
 
import psutil

import tkinter as tk
from tkinter import font


class Spoti():
    def __init__(self) -> None:
        self.API = 'https://api.spotify.com/v1/'
        self.ID='7cd206214fe74f86906ab430d1b5688d'
        self.SECRET='b272ae6335a9498ab246e10d07022738'
        self.RED_URL='http://127.0.0.1:9005'
        self.SCOPES='user-follow-read user-follow-modify streaming app-remote-control user-top-read user-read-recently-played user-read-playback-position user-library-read user-library-modify user-read-currently-playing user-modify-playback-state user-read-playback-state user-read-email user-read-private playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private ugc-image-upload'

        self.session=spoti.Spotify(auth_manager=SpotifyOAuth(client_id=self.ID,client_secret=self.SECRET,redirect_uri=self.RED_URL,scope=self.SCOPES))

        
        with open('.cache') as t:
            self.TOKEN=json.load(t)['access_token']
        

        #print(self.session.che)
        #spotify:track:1VvwxqIfKRazmvE7zdDFRg

        

        #print(self.TOKEN)
        #self.add_item_to_playlist(songs=['spotify:track:0uTEaevJy8TUD8MgzuEOc5'])
        
        # self.body={'grant_type':'client_credentials','scopes': self.SCOPES,}
        # self.response=req.post('https://accounts.spotify.com/api/token',data=self.body,auth=(self.ID,self.SECRET))
        # self.TOKEN=self.response.json()['access_token']

        # self.bd={
        #     'Content-Type':'application/json',
        #     'Authorization':'Bearer '+self.TOKEN,
        # }
        # self.response=req.get('https://api.spotify.com/v1/playlists/0c0dqQKnUr2O6nENHG3Lez?fields=tracks.items(track(name%2Cartists.name))',headers=self.bd)
        # print(self.response.json())

        #self.song_ids_from_playlist()
        #print(self.response.content)
        #print(self.TOKEN)
        #get cookie info for start_session(sp_dc, sp_key)
        #https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2F
        #self.session=spotify_token.start_session("AQBJ2V_6dHFWJJ30ZDzXTkk6O8rqlPdDRX3KAR8pQpucSOUFmVICWjvbr8Uk8h6fORhJ-iJ3EYoAMZvoAJIiycD7NCW5Js1OLdZVAh926KmEdQ","6f6ec96d-685c-41e6-8d51-65f9fb0867ca")
        #self.TOKEN=self.session[0]
        #print(self.session.playlist_tracks(playlist_id='0XEZPioQQwZfuiTpVAGNlp',fields='itemss'))
        #self.remove_item_from_playlist(songs=['3Dzso9Q2WwupEclqgxBZht'])
        #self.song_names_from_playlist() 





    def items_in_saved_check(self,songs=[]):
        return list(req.get('https://api.spotify.com/v1/me/tracks/contains?ids='+','.join(songs),headers={'Authorization':f'Bearer {self.TOKEN}'}).json())


    def current_song(self):
        return self.session.current_playback()


    def current_song_id(self) -> str:
        try:
            return self.current_song()['item']['id']
        except:
            print('NO SONG IS PLAYING')


    def song_name(self,song=None) -> str:
        if song==None:
            song=self.current_song()['item']
        elif isinstance(song,str):
            song=self.session.track(song)
        artists=''
        for i in song['artists']:
            artists+=i['name']+", "
        artists=artists[:len(artists)-2]

        return song['name'] + ' - '+ artists
    

    def song_ids_from_playlist(self,playlist='0c0dqQKnUr2O6nENHG3Lez'):
        raw=self.session.playlist(playlist_id=playlist,fields='tracks.items(track(id))')
        ids=[]
        for i in raw['tracks']['items']:
            ids.append(i['track']['id'])

        return ids


    def add_items_to_liked(self,songs=[]):
        check=self.items_in_saved_check(songs)

        for i in range(len(songs)):
            if check[i]==False:
                self.session.current_user_saved_tracks_add([songs[i]])
                print(self.song_name(songs[i]) + " - ADDED TO LIKED SONGS")
            else:
                print(self.song_name(songs[i]) + " - IS ALREADY IN LIKED SONGS")


    def add_current_to_playlist(self,playlist='0c0dqQKnUr2O6nENHG3Lez'):
        self.add_items_to_playlist(songs=[self.current_song_id()],playlist=playlist)

    def remove_current_from_playlist(self,playlist='0c0dqQKnUr2O6nENHG3Lez'):
        self.remove_items_from_playlist(songs=[self.current_song_id()],playlist=playlist)
    
    def add_current_to_liked(self):
        self.add_items_to_liked(songs=[self.current_song_id()])



    def add_items_to_playlist(self,songs,playlist='0c0dqQKnUr2O6nENHG3Lez'):
        pl_songs=self.song_ids_from_playlist(playlist=playlist)
        for i in songs:
            if i not in pl_songs:
                self.session.playlist_add_items(playlist,songs)
                print(self.song_name(song=i)+' ADDED TO PLAYLIST')
            else:
                print(self.song_name(song=i)+' IS ALREADY IN PLAYLIST')


    def remove_items_from_playlist(self,songs=[],playlist='0c0dqQKnUr2O6nENHG3Lez'):
        pl_songs=self.song_ids_from_playlist(playlist=playlist)
        for i in songs:
            if i in pl_songs:
                self.session.playlist_remove_all_occurrences_of_items(playlist,songs)
                print(self.song_name(song=self.session.track(i))+' REMOVED FROM PLAYLIST')
            else:
                print(self.song_name(song=self.session.track(i))+' NOT EXISTS IN PLAYLIST')
        



spotify=Spoti()


print('SPOTIFY LIST UPDATER')


def press(key):
    try:
        k = key.char 
    except:
        k = key.name
    if k =="f7":
        spotify.remove_current_from_playlist(playlist='0XEZPioQQwZfuiTpVAGNlp')
    elif k == '+':
        spotify.add_current_to_liked()
    elif k=='f8':
        spotify.add_current_to_playlist(playlist='0XEZPioQQwZfuiTpVAGNlp')
    elif k =='f9':
        exit()




def process_exists(processName):
    return processName in (p.name() for p in psutil.process_iter())

if(not process_exists("Spotify.exe")):
    subprocess.run(r"C:\Users\sando\AppData\Roaming\Spotify\Spotify.exe")  
 
with keyboard.Listener(on_press=press) as listener:
    listener.join()





        #print(self.TOKEN)
        #self.add_item_to_playlist(songs=['spotify:track:0uTEaevJy8TUD8MgzuEOc5'])
        
        # self.body={'grant_type':'client_credentials','scopes': self.SCOPES,}
        # self.response=req.post('https://accounts.spotify.com/api/token',data=self.body,auth=(self.ID,self.SECRET))
        # self.TOKEN=self.response.json()['access_token']

        # self.bd={
        #     'Content-Type':'application/json',
        #     'Authorization':'Bearer '+self.TOKEN,
        # }
        # self.response=req.get('https://api.spotify.com/v1/playlists/0c0dqQKnUr2O6nENHG3Lez?fields=tracks.items(track(name%2Cartists.name))',headers=self.bd)
        # print(self.response.json())

        #self.song_ids_from_playlist()
        #print(self.response.content)
        #print(self.TOKEN)
        #get cookie info for start_session(sp_dc, sp_key)
        #https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2F
        #self.session=spotify_token.start_session("AQBJ2V_6dHFWJJ30ZDzXTkk6O8rqlPdDRX3KAR8pQpucSOUFmVICWjvbr8Uk8h6fORhJ-iJ3EYoAMZvoAJIiycD7NCW5Js1OLdZVAh926KmEdQ","6f6ec96d-685c-41e6-8d51-65f9fb0867ca")
        #self.TOKEN=self.session[0]
        #print(self.session.playlist_tracks(playlist_id='0XEZPioQQwZfuiTpVAGNlp',fields='itemss'))
        #self.remove_item_from_playlist(songs=['3Dzso9Q2WwupEclqgxBZht'])
        #self.song_names_from_playlist() 


