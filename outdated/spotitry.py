from pynput import keyboard
import sys
import os
#os.system(r"C:\Users\sando\Desktop\sketchSpotifyWork\OBSCurrentSong.exe")
import subprocess
check=open("myList.txt","a")
check.close()
si=subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW


import psutil
def process_exists(processName):
    return processName in (p.name() for p in psutil.process_iter())


def setData(path,data):
    with open(path,"w",encoding='utf8')as file:
        file.write(data)

def getData(path):
    with open(path,"r",encoding='utf8') as file:
        out=""
        lines=file.read().split("\n")
        flag=False
        if lines[0]!="":
            if lines[0]=='<->':
                flag=False   
            if lines[0]=='<----->':
                flag=True   
            out+=lines[0]
        for line in range(1,len(lines)):
            if lines[line]=='<->':
                flag=False
                out+="\n"+'<->'
            if lines[line]=='<----->':
                flag=True
                out+="\n"+'<----->'
            if lines[line]!="" and lines[line]!='<----->' and lines[line]!='<->':
                if flag==True:
                    out+="\n\t"+lines[line].strip()
                else:
                    out+="\n"+lines[line].strip()
        #print (out)
        return out
    
def removeSong():
    global count
    database=getData("myList.txt")
    newSong=getData("currentsong.txt")
    if newSong in database:
        datanew=database.replace(newSong,"")
        if datanew!=database:
            database=datanew
            if count-1>=0:
                count-=1
        setData("myList.txt",database)
        database=getData("myList.txt")
        setData("myList.txt",database)
        #print("SONG:\n"+newSong+"\nDELETED FROM LIST...")
        return
    #print("LIST HAS NO SONG WITH THIS NAME")
    
def addSong():
    database=getData("myList.txt")
    newSong=getData("currentsong.txt")
    if newSong not in database:
        global count
        count+=1
        if database=="":
            setData("myList.txt",newSong)
        else:
            setData("myList.txt",database+"\n"+newSong)
            database=getData("myList.txt")
            setData("myList.txt",database)
        #print("SONG:\n"+newSong+"\nADDED TO LIST")
        return
    #print("SONG ALREADY IN LIST")
count=0
def press(key):
    try:
        k = key.char 
    except:
        k = key.name
    if k =="f8":
        removeSong()
    elif k =='f9':
        subprocess.call("taskkill /f /im OBSCurrentSong.exe",startupinfo=si)
        subprocess.call(r"taskkill /f /im Spotify.exe",startupinfo=si)
        database=getData("myList.txt")
        if count>0 or database.split("\n")[-1]!="<->":
            database+="\n<->"
            setData("myList.txt",database)
        exit(0)
    elif k == '+':
        addSong()
    elif k =="end":
        subprocess.Popen(["notepad.exe", "myList.txt"])
    else:
        print(k)


listener = keyboard.Listener(on_press=press)
listener.start()


#subprocess.call(r"C:\Users\sando\Desktop\sketchSpotifyWork\OBSCurrentSong.exe")
if(not process_exists("OBSCurrentSong.exe")):
    subprocess.call(r"start /MIN E:\utils\sketchSpotifyWork\OBSCurrentSong.exe",shell=True)
if(not process_exists("Spotify.exe")):
    os.startfile(r"C:\Users\sando\AppData\Roaming\Spotify\Spotify.exe")
listener.join()


