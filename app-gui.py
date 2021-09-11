from logging import setLoggerClass
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
            self.TOKEN=json.load(t)['refresh_token']
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

    def current_song(self):
        return self.session.current_playback()
    def current_song_id(self) -> str:
        return self.current_song()['item']['id']


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

            # name=i['track']['name']+' - '
            # for j in i['track']['artists']:
            #     name+=j['name']+', '
            # name=name[:len(name)-2]
            ids.append(i['track']['id'])
        return ids





    def add_current_to_playlist(self,playlist='0c0dqQKnUr2O6nENHG3Lez'):
        self.add_item_to_playlist(songs=[self.current_song_id()],playlist=playlist)

    def remove_current_from_playlist(self,playlist='0c0dqQKnUr2O6nENHG3Lez'):
        self.remove_item_from_playlist(songs=[self.current_song_id()],playlist=playlist)




    def add_item_to_playlist(self,songs,playlist='0c0dqQKnUr2O6nENHG3Lez'):
        pl_songs=self.song_ids_from_playlist(playlist=playlist)
        for i in songs:
            if i not in pl_songs:
                self.session.playlist_add_items(playlist,songs)
                print(self.song_name(song=i)+' ADDED FROM PLAYLIST')
            else:
                print(self.song_name(song=i)+' IS ALREADY IN PLAYLIST')


    def remove_item_from_playlist(self,songs=[],playlist='0c0dqQKnUr2O6nENHG3Lez'):
        pl_songs=self.song_ids_from_playlist(playlist=playlist)
        for i in songs:
            if i not in pl_songs:
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
    elif k == '+' or key=='f8':
        spotify.add_current_to_playlist(playlist='0XEZPioQQwZfuiTpVAGNlp')
    elif k =='f9':
        exit()


# class App(tk.Frame):
#     global spotify
#     def __init__(self,master=None):

        
#         #-----------------------
#         super().__init__(master)
#         self.master=master
#         master.geometry('400x300')
#         master.resizable(0, 0)
#         master.option_add('*Background','black')
#         master.option_add("*Button.Background",'black')
#         master.option_add("*Button.Foreground", "green")
        
#         self.pack()
#         self.create_widgets()
        
#         master.mainloop()
        

#     def create_widgets(self):
#         self.bottom=tk.Frame(self.master,height=150,width=400)
#         self.top=tk.Frame(self.master,height=150,width=400)
#         self.bottom_left=tk.Frame(self.bottom,height=150,width=200)
#         self.add_song=tk.Button(self.bottom_left,text='Add song',height=6,width=30,bd=1,font=10,command=spotify.add_current_to_playlist)
#         self.rem_song=tk.Button(self.bottom_left,text='Remove song',height=5,width=30,bd=1,font=10,command=spotify.remove_current_from_playlist)
        
#         self.quit=tk.Button(self.bottom, text="Quit", fg="red",height=12,width=30,bd=1,font=10,command=self.master.destroy)#exit


#         self.bottom.pack(side=tk.BOTTOM,fill=tk.BOTH)
#         self.bottom_left.pack(side=tk.LEFT)
        
#         self.view_list.pack(side=tk.LEFT)

#         self.quit.pack(side=tk.RIGHT)
#         self.add_song.pack(side=tk.TOP)
        
#         self.rem_song.pack(side=tk.BOTTOM)
        
#         self.top.pack(side=tk.TOP)
# app=App(master=tk.Tk(className=' Spotify List Updater'))




def process_exists(processName):
    return processName in (p.name() for p in psutil.process_iter())

 
with keyboard.Listener(on_press=press) as listener:
    listener.join()

if(not process_exists("Spotify.exe")):
    subprocess.run(r"C:\Users\sando\AppData\Roaming\Spotify\Spotify.exe")  

si=subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW








