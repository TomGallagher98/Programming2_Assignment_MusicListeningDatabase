from tkinter import *
from Main_Code import *
from tkinter import messagebox
class p_list():
    def __init__(self):
        self.songs = []
        self.length = 0

class song():
    def __init__(self,title, artist, album,t_length,source,date,time,session):
        self.title = title
        self.artist = artist
        self.album = album
        self.t_length = t_length
        self.source = source
        self.date = date
        self.time = time
        self.session = session

class Playlist():
    def __init__(self, playlist,user):
        self.master = playlist
        self.user = user
        self.list = p_list()

        playlist.title("Add Playlist")
        playlist.geometry("250x275+100+100")

        label = Label(playlist, text='Number of Songs')
        label.grid(row=0, column=0, pady=5)
        entry1 = Entry(playlist)
        entry1.grid(row=0, column=1)
        entry1.insert(0,1)

        title = Label(playlist, text='Song')
        title.grid(row=1, column=0)
        title_entry = Entry(playlist)
        title_entry.grid(row=1, column=1)

        artist = Label(playlist, text='Artist')
        artist.grid(row=2, column=0)
        artist_entry = Entry(playlist)
        artist_entry.grid(row=2, column=1)

        album = Label(playlist, text='Album/EP')
        album.grid(row=3, column=0)
        album_entry = Entry(playlist)
        album_entry.grid(row=3, column=1)

        t_length = Label(playlist, text='Length')
        t_length.grid(row=4, column=0)
        t_length_entry = Entry(playlist)
        t_length_entry.grid(row=4, column=1)

        source = Label(playlist, text='Source')
        source.grid(row=5, column=0)
        source_entry = Entry(playlist)
        source_entry.grid(row=5, column=1)

        date = Label(playlist, text='Date')
        date.grid(row=6, column=0)
        date_entry = Entry(playlist)
        date_entry.grid(row=6, column=1)

        time = Label(playlist, text='Time')
        time.grid(row=7, column=0)
        time_entry = Entry(playlist)
        time_entry.grid(row=7, column=1)

        session = Label(playlist, text='Session')
        session.grid(row=8, column=0)
        session_entry = Entry(playlist)
        session_entry.grid(row=8, column=1)

        add_button = Button(playlist, text='Add', command = lambda:add_songs())
        add_button.grid(row = 9, column = 0)

        undo_button = Button(playlist, text='Undo', command = lambda:undo())
        undo_button.grid(row=9, column=1)

        add_playlist = Button(playlist, text='Add Playlist', command=lambda: add_playlist())
        add_playlist.grid(row=10, column=0, columnspan = 2)

        length = Label(playlist, text = ' Current length 0')
        length.grid(row = 11, column=0)

        def add_songs():
            if int(entry1.get()) == self.list.length:
                 add_button['state'] = "disabled"
            else:
                title = title_entry.get()
                artist = artist_entry.get()
                album = album_entry.get()
                t_length = t_length_entry.get()
                source = source_entry.get()
                date = date_entry.get()
                time = time_entry.get()
                session = session_entry.get()
                x = song(title,artist,album,t_length,source,date,time,session)
                self.list.songs.append(x)
                self.list.length += 1
                length = Label(playlist, text=f'Current length {self.list.length}')
                length.grid(row=11, column=0)
        def add_playlist():
            if self.list.length == int(entry1.get()):
                for i in self.list.songs:
                    if i.date == '':
                        i.date = None

                    if i.time == '':
                        i.time = None
                    x = check_song(f'{i.title}',f'{i.artist}',f'{i.album}')
                    if check_song(f'{i.title}',f'{i.artist}',f'{i.album}') is not None:
                        add_play(x,self.user,i.source,i.date,i.time,i.session)
                        print (i.title,i.album,i.album,i.source,i.date,i.time,i.session)
                    else:
                        add_song(i.title,i.artist,i.album,i.t_length,'',user)
                        x = check_song(f'{i.title}', f'{i.artist}', f'{i.album}')
                        append_play(x,i.source,i.session)
            else:
                messagebox.showerror('Length Error', f'Error:\n Specified length and current length of playlist do not match\n Please add more songs or change specified track length')
                print ('no')
        def undo():
            del self.list.songs[-1]
            self.list.length -= 1
            length = Label(playlist, text=f'Current length {self.list.length}')
            length.grid(row=11, column=0)
            add_button['state'] = "active"