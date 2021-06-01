##Run The Program Through The Interface File
from Main_Code import add_song
import sqlite3
from datetime import datetime

    #In the assignment I have included 2 files so that the update itunes function can be viewed
    #'Music.txt' is the old file, 'MusicNew.txt' is the updated
    #first import the Old file, then the updated.
    #This might require changing the iTunes_Last_Update value in the actual database
def run_itunes_scrape(user):
    uid = user
    iTunes_music = []
    def get_latest_itunes(uid):  # gets the current users last spotify update day/time
        conn = sqlite3.connect('MLDB.db')
        cursorObj = conn.cursor()
        cursorObj.execute(f'select iTunes_Last_Update from user where id = {uid} ')
        timestamp = cursorObj.fetchall()[0]

        new_date_time = []
        d1 = timestamp[0].split(' ')[0]  # splits the timestamp at the space takes the first section
        d2 = d1.split('-')  # splits the date values at the - symbols
        for i in d2:  # appends the values to the new_date_time list
            new_date_time.append(i)
        t = timestamp[0].split(' ')[1]  # splits the timestamps at the space and takes the second section
        t1 = t.split(':')[0], t.split(':')[1]  # splits the time value at the : symbol and takes the first 2 values
        for i in t1:  # appends the values to new_date_time list
            new_date_time.append(i)
        return (new_date_time)
        # new_date_time list is also in Year Month Day Hour Minute
    def join_date_time(d, t):  # creates a list of each date and time value so they can be compared
        new = []
        d1 = d.split('/')  # splits date at every / divisor
        d1.reverse()  # reverses the list so that it is in YYYY MM DD order
        for i in d1:  # adds each element to the new list
            new.append(i)
        t0 = t.split(' ')
        t1 = t0[0].split(':')  # splits time at :
        for i in t1:  # appends the values to the new list
            new.append(i)
        if t0[1] == 'PM':
            x = (int(new[3]))
            x += 12
            new[3] = str(x)
        return (new)

    def check_last_update(latest,new):
        d = new.split(' ')[0]
        t0 = new.split(' ')[1],new.split(' ')[2]
        t = ' '.join(t0)
        date_time = join_date_time(d,t)
        count = 0
        for t in range(0, len(date_time)):
            # loop keeps running if the values are the same
            if count < 5:  # as soon as one value is greater the code will stop comparing the rest of the values
                if int(latest[t]) < int(date_time[t]):
                    count += 5  # if any of the values are greater 5 is added to the count
                elif int(latest[t]) > int(date_time[t]):
                    break
        if count == 5:
            return (date_time)
    # first need to export list of songs to a text file, I could find no other way to read the data
    # when exported the songs should be in order of last play date/time
    # opens the text file to read, the file is written in UTF 16 so needs to be specified
    def get_file(uid): # finds the users iTunes file name
        conn = sqlite3.connect('MLDB.db')
        cursorObj = conn.cursor()
        cursorObj.execute(f'select iTunes from user where id = {uid} ')
        iTunes_file = cursorObj.fetchall()[0]
        return iTunes_file[0]
    itunes_file = get_file(uid)
    with open(itunes_file, mode='r', encoding='utf-16') as music:
        Last_Update = get_latest_itunes(uid)
        head = []
        for x in range(500):
            i = next(music).split('\t')
            if i[22] == 'Last Played':
                pass  # skips the heading element in the file
            elif check_last_update(Last_Update, i[22]) == None:
                break  # breaks the loop. This also stops the program from needing to sort through the entire song list
            else:  # appends the song to the Music List
                iTunes_music.insert(0,[i[0],i[1],i[3],i[5],i[7],i[21],i[22]])
                head.append(i[22])

    def find_base_plays(song, uid):  # Finds base plays of a song
        conn = sqlite3.connect('MLDB.db')
        cursorObj = conn.cursor()
        cursorObj.execute(f'select p.itunes_Base_Plays from Plays p join Song s on p.Song = s.id where p.User_ID = {uid} and s.Title = "{song}" and p.itunes_Base_Plays != "None"')
        Base = cursorObj.fetchall()
        if Base == []: # sets the base to 0 if there is no previous instance
            Base= (0,)
        else:
            Base = Base[0]
        cursorObj = conn.cursor()  # finds every instance of the song in the database where the source is itunes
        cursorObj.execute(f'select count(*) from Plays p join Song s on p.Song = s.id where p.User_ID = {uid} and s.Title = "{song}" and p.Source = "iTunes"')
        Inst = cursorObj.fetchall()[0]

        return Base[0],Inst[0]

    def write_to_db(songs):
        for song in songs:  # iterates through the songs to be added list
            base = find_base_plays(song[0],uid)  # returns the base plays for each song
            # standardises the time from the file into hh:mm
            min = int(song[4])//60
            sec = int(song[4])-(min*60)
            length = str(min) + ':' + str(sec)
            dt = song[-1].split(' ')
            date = dt[0]  # the date is already in the standardized format
            time = dt[1]
            if dt[2] == 'PM': # adds 12 hours when the time is in 12H time and after 12 pm
                x = (time.split(':'))
                y = int(x[0])
                if y != 12:
                    y += 12
                x[0] = str(y)
                time = ':'.join(x)
            if base[0] == 0:  # only adds the song once if the itunes base is 0, as it is the first play
                add_song(song[0], song[1], song[2], length, song[3], 2, date, time, 'iTunes', song[5])
            else:  # calculates the difference between the current itunes plays and base itunes plays
                # adds the song as many times as the calculated difference is
                plays = int(song[5]) - (int(base[0])+int(base[1])-1)
                for i in range (0,plays):
                    add_song(song[0],song[1],song[2],length,song[3],2,date,time,'iTunes')

        # updates the itunes last update if there were any songs to update
        if len(songs) > 0:
            last_update = datetime.now()
            conn = sqlite3.connect('MLDB.db', timeout=5)
            cursorObj = conn.cursor()
            cursorObj.execute(
                f"UPDATE User set iTunes_Last_Update = '{last_update}' where id = {uid}")
            conn.commit()

    write_to_db(iTunes_music)

