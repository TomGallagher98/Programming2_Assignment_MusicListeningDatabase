from datetime import datetime
from dateutil import tz
import sqlite3


###SPOTIFY SAMPLES####
def Duration_MS_to_MINSECS(ms):  # converts the track length from milliseconds to mm:ss format
    min = ms // 60000  # calculates the minute value
    sec = (
                      ms - min * 60000) // 1000  # removes only the minute value and calculates the seconds value from the remaining time
    if len(str(sec)) < 2:  # adds the leading 0 to single digit numbers for storage
        sec = '0' + str(sec)
        duration = str(min) + ':' + sec  # joins the minutes and seconds into one string
    else:  # joins the minutes and seconds into one string
        duration = str(min) + ":" + str(sec)
    return duration  # returns the duration so it can be used later in the code

def Date_Time_Separate(dt):  # separates the Spotify date and time format ('2021-05-21T22:39:36.218Z')
    # first converts the spotify time (UTC) to local time
    d = (dt.split('T')[0])  # splits at the T and returns only the first value (the date)
    t0 = dt.split('T')[1]  # returns the second half of the T split
    t1 = t0.split(':')[0], t0.split(':')[1]  # splits at : and returns only the first and second values (mm,ss)
    time_split = ':'.join(t1)  # joins the list into string mm:ss
    dt2 = d + ' ' + time_split  # joins the 2 strings so that they can be interpreted by the utc, tz and datetime commands
    from_zone = tz.tzutc()  # sets the from time as utc
    to_zone = tz.tzlocal()  # sets the time zone to convert to as the local time zone
    utc = datetime.strptime(dt2, '%Y-%m-%d %H:%M')
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    # seprates the date and time
    d1 = str(central).split(' ')[0]
    d2 = d1.split('-')
    d2.reverse()  # reverses the list so it is now in [dd,mm,yyyy]
    date_split = '/'.join(d2)  # joins the list into string dd/mm/yyyy
    t2 = str(central).split(' ')[1]
    t3 = t2.split(':')[0], t2.split(':')[1]
    time_split = ':'.join(t3)
    return date_split, time_split

def join_date_time(d, t):  # creates a list of each date and time value so they can be compared
    new = []
    d1 = d.split('/')  # splits date at every / divisor
    d1.reverse()  # reverses the list so that it is in YYYY MM DD order
    for i in d1:  # adds each element to the new list
        new.append(i)

    t1 = t.split(':')  # splits time at :
    for i in t1:  # appends the values to the new list
        new.append(i)
    #Added to test the itunes functions
    t0 = t.split(' ')
    if t0[-1] == 'PM':
        x = (int(new[3]))
        x += 12
        new[3] = str(x)
    return (new)
    # each subsequent element in the list is smaller Year Month Day Hour Minute

def get_latest_spotify(uid): #gets the current users last spotify update day/time
    conn = sqlite3.connect('MLDB.db')
    cursorObj = conn.cursor()
    cursorObj.execute(f'select Spotify_Last_Update from user where id = {uid} ')
    timestamp = cursorObj.fetchall()[0]

    new_date_time = []
    d1 = timestamp[0].split(' ')[0] #splits the timestamp at the space takes the first section
    d2 = d1.split('-') #splits the date values at the - symbols
    for i in d2: #appends the values to the new_date_time list
        new_date_time.append(i)
    t = timestamp[0].split(' ')[1] #splits the timestamps at the space and takes the second section
    t1 = t.split(':')[0], t.split(':')[1] #splits the time value at the : symbol and takes the first 2 values
    for i in t1: #appends the values to new_date_time list
        new_date_time.append(i)
    return (new_date_time)

###ITUNES SAMPLES####
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
def get_file(uid, Last_Update):
    iTunes_music = []
    conn = sqlite3.connect('MLDB.db')
    cursorObj = conn.cursor()
    cursorObj.execute(f'select iTunes from user where id = {uid} ')
    iTunes_file = cursorObj.fetchall()[0]


    with open(iTunes_file[0], mode='r', encoding='utf-16') as music:

        head = []
        for x in range(11): #In actual code range is 500
            i = next(music).split('\t')

            if i[22] == 'Last Played':
                pass #skips the heading element in the file
            elif check_last_update(Last_Update, i[22]) == None:
                break  #breaks the loop. This also stops the program from needing to sort through the entire song list
            else: #appends the song to the Music List
                iTunes_music.insert(0,[i[0],i[1],i[3],i[5],i[7],i[21],i[22]])
                head.append(i[22])

        return (len(iTunes_music), iTunes_music)
