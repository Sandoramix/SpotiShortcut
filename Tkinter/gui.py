import tkinter as tk



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
