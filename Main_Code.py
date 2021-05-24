#Code the main interface page to allow it to connect with the database

import sqlite3
from datetime import datetime, timedelta

def get_user_id(username): #used when the user logs in so that the program can find their username for later commands
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
        f"select Song.Length from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid} and Song.Artist = '{artist}'")
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


def add_play(sid,uid,source=None,date=None,time=None,session=None):
    #adds a date and time if they are left blank when entering a play, so that date and time can be used in later code
    if date is None:
        today = datetime.now()
        date = today.strftime("%d/%m/%Y")
    if time is None:
        now = datetime.now()
        time = now.strftime('%H:%M')
    #source and session can be left blank
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    p_id = len(cursorObj.execute("select * from Plays").fetchall()) + 1 #adds a unique play id
    cursorObj.execute(
        f"INSERT INTO Plays VALUES({p_id}, '{sid}', '{source}', '{date}', '{time}', '{session}','{uid}')")
    conn.commit()
    conn.close()

def append_play(sid,source,session): #allows the user to add the source and session to a play
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute(
        f"UPDATE Plays Set source = '{source}',session = '{session}' where Song = {sid}")
    conn.commit()
    conn.close()

def add_song(Title,Artist,Album,Length,Genre,User_Id, date = None, time = None, source = None):
    #if the song is already in the database it is added automatically to plays
    if check_song(Title,Artist,Album) is not None:
        sid = check_song(Title,Artist,Album)
        add_play(sid, User_Id, source=source,date=date, time=time)
    else:
        #the song is written into the songs table before being added into the plays table
        conn = sqlite3.connect('MLDB.db', timeout=10)
        cursorObj = conn.cursor()
        sid = len(cursorObj.execute("select * from Song").fetchall()) + 1 #ensures the song is given a unique id for the database
        cursorObj.execute(
            f'INSERT INTO Song VALUES({sid}, "{Title}", "{Artist}", "{Album}", "{Length}", "{Genre}")')
        conn.commit()
        conn.close()
        add_play(sid, User_Id, source=source,date=date, time=time)

def music_stats(uid, artist = None, album = None):
    #adding an artist or album will restrict the code to be implemented on only the artist or album
    if artist is not None: #when there is an artist the code is run on the artist
        conn = sqlite3.connect('MLDB.db', timeout=5)
        cursorObj = conn.cursor()
        cursorObj.execute( #returns the song name, its total plays and the the artist, the results are sorted descending by total plays
            f"select Song.Title, count(*), Song.Artist as c from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid} and Song.Artist ='{artist}' group by Song.id order by c desc, Song.Length desc")
        user = cursorObj.fetchall()
        conn.commit()
        conn.close()
        return user[0][0] #returns only the top result, which is the result with the most plays
    if album is not None: #when there is an album the code is run on the album
        conn = sqlite3.connect('MLDB.db', timeout=5)
        cursorObj = conn.cursor()
        cursorObj.execute( #returns the song name, its total plays and the album, the results are sorted descending by total plays
            f"select Song.Title, count(*) as c , Song.Album from Song join Plays on Song.id = Plays.Song where Plays.User_id = {uid} and Song.Album ='{album}' group by Song.id order by c desc, Song.Length desc")
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
    print(artist)
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

def source_stats(uid): #finds the most used source of music
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute(
        f"select count(*) as c, Source from Plays where User_id = {uid} group by Source order by c desc")
    source = cursorObj.fetchall()
    conn.commit()
    source_type = source[0][1]
    cursorObj = conn.cursor()
    cursorObj.execute(
        f"select count(*) as c, Song.Title from Song join Plays on Song.id = Plays.Song where Plays.Source like '{source_type}' group by Song.id order by c desc")
    song = cursorObj.fetchall()
    conn.commit()
    song_title = song[0][1]  #returns the most listened to song on the source
    conn.close()
    return (source_type, song_title)

def session_stats(uid): #finds the most frequent session
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    cursorObj.execute(
        f"select count(*) as c, Session from Plays Where User_id = {uid} and Session not like 'None' group by Session order by c desc")
    session = cursorObj.fetchall()
    conn.commit()
    session_type = session[0][1]
    cursorObj = conn.cursor()
    cursorObj.execute( #finds the most frequently listened to song during the session type
        f"select count(*) as c, Song.Title from Song join Plays on Song.id = Plays.Song where Plays.Session like '{session_type}' group by Song.id order by c desc")
    song = cursorObj.fetchall()
    conn.commit()
    song_title = song[0][1] #returns the song name
    conn.close()
    return (session_type, song_title)



