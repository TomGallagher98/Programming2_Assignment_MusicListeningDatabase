##Run The Program Through The Interface File
from tkinter import *

#Displays the users most played song, and its total plays
class Song_Stat_Window():
    def __init__(self, stats, song, plays, artist):
        self.master = stats
        self.song = song
        self.plays = plays
        self.artist = artist

        stats.title("Song Stats")
        stats.geometry("200x200+100+100")

        label = Label(stats, text = 'Song Statistics')
        label.grid(row = 0, pady=10)

        label2 = Label(stats, text="Your most played song is:")
        label2.grid(row=1,pady=5)

        label3 = Label(stats, text=f"{song} by {artist}")
        label3.grid(row=2)

        label4 = Label(stats, text=f"Total Listens: {plays}")
        label4.grid(row=3,pady=10)


# displays the most played artist, how many total listens and most frequent song
class Artist_Stats_Window():
    def __init__(self, stats, artist, times, song):
        self.master = stats
        self.artist = artist
        self.times = times
        self.song = song

        stats.title = 'Artist Stats'
        stats.geometry("300x200+100+100")

        label = Label(stats, text='Artist Statistics')
        label.grid(row=0, pady=10)

        label2 = Label(stats, text="Your most played artist is:")
        label2.grid(row=1, pady=5)

        label3 = Label(stats, text=f"{artist}")
        label3.grid(row=2)

        label4 = Label(stats, text=f"Total time: {times}")
        label4.grid(row=3, pady=10)

        label5 = Label(stats, text=f"Your most played song by {artist} is:")
        label5.grid(row=4, pady=5)

        label6 = Label(stats, text=f"{song}")
        label6.grid(row=5)


#shows most listened to album and most listened to song on the album
class Album_Stats_Window():
    def __init__(self, stats, album, artist, song):
        self.master = stats
        self.song = song
        self.album = album
        self.artist = artist

        stats.title("Album Statistics")
        stats.geometry("300x200+100+100")

        label = Label(stats, text = 'Album Statistics')
        label.grid(row = 0, pady=10)

        label2 = Label(stats, text="Your most played album is:")
        label2.grid(row=1,pady=5)

        label3 = Label(stats, text=f"{album} \n by {artist}")
        label3.grid(row=2)

        label4 = Label(stats, text=f"Your most listened to song on {album} is {song}")
        label4.grid(row=3,pady=10)


# shows most played song for the selected source
class Source_Details():
    def __init__(self,stats,source,song, plays):
        self.master = stats
        self.source = source
        self.song = song

        stats.title("Source Statistics")
        stats.geometry("300x200+100+100")

        label = Label(stats, text=f'{source} Statistics')
        label.grid(row=0, pady=10)

        label3 = Label(stats, text=f"Your most frequent song on {source} is:")
        label3.grid(row=2)

        label4 = Label(stats, text=f"{song} with {plays} plays")
        label4.grid(row=3)


# Displays most played song for each session
class Session_Details():
    def __init__(self,stats,session,song, plays):
        self.master = stats
        self.session = session
        self.song = song

        stats.title("Session Statistics")
        stats.geometry("300x200+100+100")

        label = Label(stats, text=f'{session} Statistics')
        label.grid(row=0, pady=10)

        label3 = Label(stats, text=f"Your most frequent song during {session} was:")
        label3.grid(row=2)

        label4 = Label(stats, text=f"{song} with {plays} plays")
        label4.grid(row=3)