##Run The Program Through The Interface File

import sqlite3
from datetime import datetime, timedelta,date
from Login_Access import *
from tkinter import *
from Stat_Windows import Session_Details, Source_Details


def get_user_id(username): # used when the user logs in so that the program can find their username for later commands
    conn = sqlite3.connect('MLDB.db')
    cursorObj = conn.cursor()
    cursorObj.execute('select id, username from user')
    all_rows = cursorObj.fetchall()
    for user in all_rows:
        # usernames are unique so matching the entered username with a username will produce the correct list
        if username == user[1]:
            return user[0] #returns only the id

def song_count(uid): #selects all the unique values from the plays table, filters out all results of other users
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute(
        f"select count(DISTINCT Song) from Plays where User_id = {uid}")
    songs = cursorObj.fetchall()
    conn.commit()
    conn.close()
    return songs[0][0] #returns only the value corresponding to total songs

def secondize(times):
    # splits the times into seconds and minutes, converts the minutes into seconds, then sums all the values in both lists and returns the sum of the two values
    mins = [int(i[0].split(':')[0]) for i in times]
    secs = [int(i[0].split(':')[1]) for i in times]
    m_s = [i * 60 for i in mins]
    tot = sum(m_s) + sum(secs)
    return timedelta(seconds=tot)

def get_time(uid): #sorts through the users plays and sums all the times of the songs.
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute(
        f"select Song.Length from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid}")
    times = cursorObj.fetchall()
    conn.commit()
    conn.close()
    # returns the times of all the songs as a list
    return (secondize(times))

def get_artist_time(uid, artist):
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute(
        f"select Song.Length from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid} and Song.Artist = :a",{"a":artist})
    times = cursorObj.fetchall()
    conn.commit()
    conn.close()
    # returns the times of all the songs as a list
    return (secondize(times))

def check_song(title, artist, album): #used by the "ADD_SONG" command, to ensure no song can be added twice
    conn = sqlite3.connect('MLDB.db', timeout = 5)
    cursorObj = conn.cursor()
    cursorObj.execute('select id,Title,Artist,Album from Song')
    all_rows = cursorObj.fetchall()
    for song in all_rows:
        # using indexes ensures the username is matched with the username and the same with the password
        if title == song[1] and artist == song[2] and album == song[3]:
            return song[0]
            #returns the songs id so that it can be added into the Plays table

def add_play(sid,uid,source=None,date=None,time=None,session=None, itunes_Base_Plays=None):
    #adds a date and time if they are left blank when entering a play,
    #checks that the date and time are in the correct format
    #if the date and time are blank they are set to 0 so that the check_format code will work
    if date == None:
        date = '0'
    if time == None:
        time = '0'
    date = check_formats(date1=date)
    time = check_formats(time1=time)
    #source and session can be left blank

    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    p_id = len(cursorObj.execute("select * from Plays").fetchall()) + 1 #adds a unique play id
    cursorObj.execute(
        f"INSERT INTO Plays VALUES({p_id}, '{sid}', :so, :d, :t, :se,'{uid}', :i)",{'so':source,'d':date,'t':time,'se':session,'i':itunes_Base_Plays})
    conn.commit()
    conn.close()

def append_play(sid,source,session): #allows the user to add the source and session to a play
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute(
        f"UPDATE Plays Set source = :so ,session = :se where Song = {sid}",{"so":source, "se":session})
    conn.commit()
    conn.close()

def check_formats(length = None, date1 = None, time1 = None):
    if length != None: #Formats the length of the track into a standard length
        try:
            for i in length:
                if i != ':':
                    int(i)
        except: #If there is a value that is not a digit or :, then the song length is set to the average song length
            ValueError
            length = '3:30'
            return length #returns the length and breaks
        a = length.split(':')
        if len(a) == 2: #when the length is in the correct format it is automatically returned
            if a[0] == '':
                length = '0' + length
            if a[1] == '':
                length = length + '00'
            return length
        elif len(a) == 1: #if there is no : break in the length, one is added
            a = ' '.join(a[0])
            a = a.split(' ')
            if len(a) == 4: #changes the format to mm:ss
                m = [a[0], a[1]]
                m = ''.join(m)
                s = a[2], a[3]
                s = ''.join(s)
                d = [m, s]
                length = ':'.join(d)
            elif len(a) == 3: #changes the format to m:ss
                try:
                    m = a[0]
                    s = a[1], a[2]
                    s = ''.join(s)
                    d = [m, s]
                    length = ':'.join(d)
                except:#incase of consective :: separators
                    ValueError
                    length = '3:30'
            elif len(a) == 2: #changes the format to m:ss
                length = '0:' + length
            else: #anything longer than 4 digits is assumed to be a mistake so length is set to average length
                length = '3:30'
        elif len(a) == 3: #if there are 2 ':' breaks it is assumed the front is in hours.
            #the hours gets changed to minutes so the format will be mm:ss
            try:
                h = a[0]
                m0 = a[1]
                m = (int(h) * 60) + int(m0)
                print(m)
                b = [str(m), a[2]]
                length = ':'.join(b)
            except:
                ValueError
                length = '3:30'
        else: #for any other unusual format the length is set automatically to the average length
            length = '3:30'
        return length
    # checks that the date is in the format dd/mm/yyyy
    # date is set to current date if there are any format errors
    if date1 != None:
        date1 = str(date1)
        if len(date1.split('/')) == 3:  # checks that there are 3 values after being split
            try: # If there is a value that is not a digit or /, then the date is set to today
                for i in date1:
                    if i != '/':
                        int(i)
            except:
                ValueError
                date1 = date.today()
                date1 = date1.strftime("%d/%m/%Y")
                return date1  # returns the date and breaks
            day, month, year = date1.split('/')
            try: #checks that the date is in a proper format
                datetime(int(year), int(month), int(day))
                return (date1)
            except ValueError: #sets the date to today if there is an error in the format
                date1 = date.today().strftime("%d/%m/%Y")
                return date1
        else:
            date1 = date.today().strftime("%d/%m/%Y")
            return date1
    # checks that the time is in the format hh:mm
    # time is set to current time if there are any format errors
    if time1 != None:
        time1 = str(time1)
        if len(time1.split(':')) == 2:
            try:
                for i in time1:
                    if i != ':':
                        int(i)
            except ValueError:  # If there is a value that is not a digit or : then the time is set to the current time
                time1 = datetime.now().strftime("%H:%M")
                return time1
            # splits the time and checks that the minutes are below 60 and hours below 24
            #returns the time if they are, returns the current time if they are not
            try:
                hour,min = time1.split(':')
                if int(min) < 60 and int(hour) < 24:
                    return (time1)
                else:
                    time1 = datetime.now().strftime("%H:%M")
                    return time1
            except ValueError:
                time1 = datetime.now().strftime("%H:%M")
                return time1
        else:
            time1 = datetime.now().strftime("%H:%M")
            return time1

def add_song(Title,Artist,Album,Length,Genre,User_Id, date = None, time = None, source = None, itunes_Base_Plays = None):
    #if the song is already in the database it is added automatically to plays
    if check_song(Title,Artist,Album) is not None:
        sid = check_song(Title,Artist,Album)
        add_play(sid, User_Id, source=source,date=date, time=time,itunes_Base_Plays=itunes_Base_Plays)
    else:
        Length = check_formats(length = Length)
        #the song is written into the songs table before being added into the plays table
        conn = sqlite3.connect('MLDB.db', timeout=10)
        cursorObj = conn.cursor()
        sid = len(cursorObj.execute("select * from Song").fetchall()) + 1 #ensures the song is given a unique id for the database
        cursorObj.execute(
            f'INSERT INTO Song VALUES({sid}, :t, :a, :al, :l, :g)',{"t":Title,"a":Artist, "al":Album, "l":Length, "g":Genre})
        conn.commit()
        conn.close()

        add_play(sid, User_Id, source=source,date=date, time=time,itunes_Base_Plays=itunes_Base_Plays)
    return 'Yes'

def music_stats(uid, artist = None, album = None):
    #adding an artist or album will restrict the code to be implemented on only the artist or album
    if artist is not None: #when there is an artist the code is run on the artist
        conn = sqlite3.connect('MLDB.db', timeout=5)
        cursorObj = conn.cursor()
        cursorObj.execute( #returns the song name, its total plays and the the artist, the results are sorted descending by total plays
            f"select Song.Title, count(*)  as c, Song.Artist from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid} and Song.Artist = :a group by Song.id order by c desc, Song.Length desc",{'a':artist})
        user = cursorObj.fetchall()
        conn.commit()
        conn.close()
        return user[0][0] #returns only the top result, which is the result with the most plays
    if album is not None: #when there is an album the code is run on the album
        conn = sqlite3.connect('MLDB.db', timeout=5)
        cursorObj = conn.cursor()
        cursorObj.execute( #returns the song name, its total plays and the album, the results are sorted descending by total plays
            f"select Song.Title, count(*) as c , Song.Album from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid} and Song.Album = :a group by Song.id order by c desc, Song.Length desc",{"a":album})
        user = cursorObj.fetchall()
        conn.commit()
        conn.close()
        return user[0][0] #returns only the top result, which is the result with the most plays
    else: #base code which is used on the users entire play history
        conn = sqlite3.connect('MLDB.db', timeout=5)
        cursorObj = conn.cursor()
        cursorObj.execute( #returns the song name, its total plays and the artist, the results are sorted descending by total plays
            f"select Song.Title, count(*) as c, Song.Artist from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid} group by Song.id order by c desc")#, Song.Length desc")
        user = cursorObj.fetchall()
        conn.commit()
        conn.close()
        return user[0] #returns only the top result, which is the result with the most plays

def artist_stats(uid): #finds the most played artist
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute(#returns the artist and their total playsthe results are sorted descending by total plays
        f"select count(*) as c, Song.Artist as a from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid} group by a order by c desc")
    artist = cursorObj.fetchall()
    conn.commit()
    conn.close()
    name = artist[0][1]
    times = get_artist_time(uid,name) #returns the total time spent listening to the artist
    song = music_stats(uid, artist = name) #returns the arists most played song
    return (name, times, song)

def album_stats(uid): #finds the most played album (by individual track plays)
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute( #returns the ablum name, its total plays and the artist the results are sorted descending by total plays
        f"select count(*) as c, Song.Album as a, Song.Artist from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid} group by a order by c desc")
    album = cursorObj.fetchall()
    conn.commit()
    album_name = album[0][1]
    artist = album[0][2]
    song = music_stats(uid, album = album_name) #returns the most played song from the album
    conn.close()
    return (album_name,artist,song)

def source_stats(uid, source, type): #finds the most used source of music
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()

    cursorObj.execute(
        f"select count(*) as c, Song.Title from Song join Plays on Song.id = Plays.Song where User_id = {uid} and Plays.{source} like :t group by Song.id order by c desc", {"t":type})
    song = cursorObj.fetchall()
    conn.commit()
    plays = song[0][0]
    song_title = song[0][1]  #returns the most listened to song on the source
    conn.close()
    return (source, song_title, plays)


def choice_box(uid,source):  # allows the user to choose from their current sessions/sources
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute(  # returns every source or session the user has in the database
        f"select count(*) as c, {source} from Plays where User_id = {uid} group by {source} order by c desc")
    values = cursorObj.fetchall()
    choices = [i[1] for i in values] #creates a list of all the sources/sessions
    master = Tk()

    def get_val():
        v = variable.get() #gets the currently selected variable
        stats = source_stats(uid,source,v) #runs the source stats code to retrieve the top song
        if source == 'session':
            song = stats[1]
            plays = stats[2]
            root = Tk()
            Session_Details(root, v, song, plays)
            master.destroy()
        else:
            song = stats[1]
            plays = stats[2]
            root = Tk()
            Source_Details(root, v, song, plays)
            master.destroy()

    variable = StringVar(master)  # is set to the selected variable from the list
    variable.set(choices[0])  # default value is the source/session with the most plays

    w = OptionMenu(master, variable, *choices) #every element in the choices list is set as a option in the drop down
    w.grid(row=1,column=1)

    select = Button(master, text='Select',command=get_val)
    select.grid(row=1,column=2) #runs when the user has made their choice

    mainloop()


