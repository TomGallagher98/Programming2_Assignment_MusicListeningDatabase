from tkinter import *
from Main_Code import *
from tkinter import messagebox

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

class Playlist(): #creates a GUI but also can store data
    def __init__(self, playlist,user):
        self.master = playlist
        self.user = user
        self.list = [] #songs are first added to the list, then at the end the entire playlist is written into DB
        self.length = 0 #stores the current length

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

        #adds a song to the playlist list when pressed
        add_button = Button(playlist, text='Add', command = lambda:add_songs())
        add_button.grid(row = 9, column = 0)

        #removes the last added song from the playlist list
        undo_button = Button(playlist, text='Undo', command = lambda:undo())
        undo_button.grid(row=9, column=1)

        #writes the entire playlist to the database when pressed
        add_playlist = Button(playlist, text='Add Playlist', command=lambda: add_playlist())
        add_playlist.grid(row=10, column=0, columnspan = 2)

        #shows the user how many songs are currently in the playlist
        length = Label(playlist, text = ' Current length 0')
        length.grid(row = 11, column=0)

        def add_songs(): #disables the add song button when the playlist is longer than the user specified
            if int(entry1.get()) == self.length:
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
                #retrieves all the entries and creates a song class
                x = song(title,artist,album,t_length,source,date,time,session)
                #adds the song to the list and adds one to the length count
                self.list.append(x)
                self.length += 1
                #updates the length label when a song is added
                length = Label(playlist, text=f'Current length {self.length}')
                length.grid(row=11, column=0)
        def add_playlist():
            if self.length == int(entry1.get()): #only runs when the playlist length is the specified length
                for i in self.list:
                    if i.date == '':
                        i.date = None
                        #################ADD FORMATTING CHECK############################
                        #sets the date and time to None is there is no value entered
                    if i.time == '':
                        i.time = None
                    #checks that the song is already in the database
                    x = check_song(f'{i.title}',f'{i.artist}',f'{i.album}')
                    if check_song(f'{i.title}',f'{i.artist}',f'{i.album}') is not None:
                        add_play(x,self.user,i.source,i.date,i.time,i.session)
                        #adds play if the song is already in database
                        print (i.title)
                        # print (i.title,i.album,i.album,i.source,i.date,i.time,i.session)
                    else:#adds the songs to the data base which automatically adds the play
                        add_song(i.title,i.artist,i.album,i.t_length,'',user)
                        x = check_song(f'{i.title}', f'{i.artist}', f'{i.album}')
                        #appends the source and session after the song is added
                        #because it is the first instance the song id can also be used to update the play
                        append_play(x,i.source,i.session)
            else:
                #displays an error when the length does not match
                messagebox.showerror('Length Error', f'Error:\n Specified length and current length of playlist do not match\n Please add more songs or change specified track length')
                print ('no')
        def undo(): #allows the user to remove songs from the song list
            if self.length >= 1: #only works if there are currently songs in the list
                del self.list[-1] #removes the last added entry
                self.length -= 1 #removes one from the current length
                length = Label(playlist, text=f'Current length {self.length}')
                length.grid(row=11, column=0)
                add_button['state'] = "active" #activates the add button if it was previously disabled