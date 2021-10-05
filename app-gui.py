import threading
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
import os

import tkinter as tk
from tkinter import font

class Spoti():
    
    def __init__(self) -> None:
        self.line = "-"*50+"\n"

        self.API = os.environ['API']
        self.ID=os.environ['CLIENT_ID']
        self.SECRET = os.environ['CLIENT_SECRET']
        self.RED_URL = os.environ['RED_URL']
        self.SCOPES = os.environ['SCOPES']
        self.RTOKEN=os.environ['REFRESH_TOKEN']
        
        print(f'{self.line}SPOTIFY LIST UPDATER {datetime.datetime.now()}\n{self.line}', end='')

        self.oauth = SpotifyOAuth(client_id=self.ID, client_secret=self.SECRET, redirect_uri=self.RED_URL, scope=self.SCOPES)
        self.session = spoti.Spotify(auth_manager=self.oauth)
        self.TOKEN = self.oauth.get_access_token(as_dict=False)

        threading.Thread(threading.Timer(10, self.tkn_update).start()).start()
    

    def tkn_update(self):
        print(f'{self.line}TOKEN UPDATED {datetime.datetime.now()}\n{self.line}',end='')
        self.oauth.refresh_access_token(self.RTOKEN)
        self.TOKEN = self.oauth.get_access_token(as_dict=False)

        
        


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




    def remove_items_from_liked(self,songs=[]):
        check=self.items_in_saved_check(songs)
        for i in range(len(songs)):
            if check[i]==True:
                self.session.current_user_saved_tracks_delete([songs[i]])
                print("L[True] del - "+self.song_name(songs[i]))
            else:
                print("L[False] del - "+self.song_name(songs[i]))



    def add_items_to_liked(self,songs=[]):
        check=self.items_in_saved_check(songs)
    
        for i in range(len(songs)):
            if check[i]==False:
                self.session.current_user_saved_tracks_add([songs[i]])
                
                print("L[True] add - "+self.song_name(songs[i]))
            else:
                print("L[False] add - "+self.song_name(songs[i]))


    def remove_current_from_liked(self):
        self.remove_items_from_liked(songs=[self.current_song_id()])
    def add_current_to_liked(self):
        self.add_items_to_liked(songs=[self.current_song_id()])






    def add_items_to_playlist(self,songs,playlist='0c0dqQKnUr2O6nENHG3Lez'):
        pl_songs=self.song_ids_from_playlist(playlist=playlist)
        for i in songs:
            if i not in pl_songs:
                self.session.playlist_add_items(playlist,songs)
                print("P[True] add -"+self.song_name(i))
            else:
                print("P[False] add - "+self.song_name(i))


    def remove_items_from_playlist(self,songs=[],playlist='0c0dqQKnUr2O6nENHG3Lez'):
        pl_songs=self.song_ids_from_playlist(playlist=playlist)
        for i in songs:
            if i in pl_songs:
                self.session.playlist_remove_all_occurrences_of_items(playlist,songs)
                print("P[True] del - "+self.song_name(i))
            else:
                print("P[False] del - "+self.song_name(i))
        
    def add_current_to_playlist(self, playlist='0c0dqQKnUr2O6nENHG3Lez'):
        self.add_items_to_playlist(
            songs=[self.current_song_id()], playlist=playlist)

    def remove_current_from_playlist(self, playlist='0c0dqQKnUr2O6nENHG3Lez'):
        self.remove_items_from_playlist(
            songs=[self.current_song_id()], playlist=playlist)




spotify=Spoti()



def press(key):
    try:
        k = key.char 
    except:
        k = key.name
    if k =="f7":
        spotify.remove_current_from_playlist(playlist='0XEZPioQQwZfuiTpVAGNlp')
    elif k == '+':
        spotify.add_current_to_liked()
    elif k == '-':
        spotify.remove_current_from_liked()
    elif k=='f8':
        spotify.add_current_to_playlist(playlist='0XEZPioQQwZfuiTpVAGNlp')
    elif k =='f9':
        exit()




def listener():
    with keyboard.Listener(on_press=press) as listener:
        listener.join()
threading.Thread(target=listener).start()


class App(tk.Frame):
    global spotify

    def __init__(self, master=None, spotify=None):
        if spotify == None:
            print('No spotify session acquired')
            exit()
        self.spotify = spotify
        #-----------------------
        super().__init__(master)
        self.master = master
        master.geometry('400x300')
        master.resizable(0, 0)
        master.option_add('*Background', 'black')
        master.option_add("*Button.Background", 'black')
        master.option_add("*Button.Foreground", "green")

        self.pack()
        self.create_widgets()

        master.mainloop()

    def create_widgets(self):
        self.bottom = tk.Frame(self.master, height=150, width=400)
        self.top = tk.Frame(self.master, height=150, width=400)
        self.bottom_left = tk.Frame(self.bottom, height=150, width=200)

        self.view_list = tk.Button(
            self.top, text='View List', height=6, width=50, bd=1, font=10, command=self.spotify)

        self.add_song = tk.Button(self.bottom_left, text='Add song',
                                  height=6, width=30, bd=1, font=10, command=self.spotify)
        self.rem_song = tk.Button(self.bottom_left, text='Remove song',
                                  height=5, width=30, bd=1, font=10, command=self.spotify)

        self.quit = tk.Button(self.bottom, text="Quit", fg="red", height=12,
                              width=30, bd=1, font=10, command=self.master.destroy)  # exit

        self.bottom.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.bottom_left.pack(side=tk.LEFT)

        self.view_list.pack(side=tk.LEFT)

        self.quit.pack(side=tk.RIGHT)
        self.add_song.pack(side=tk.TOP)

        self.rem_song.pack(side=tk.BOTTOM)

        self.top.pack(side=tk.TOP)
#app = App(master=tk.Tk(className=' Spotify List Updater'),spotify=spotify)


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


