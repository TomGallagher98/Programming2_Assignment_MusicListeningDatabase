import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Main_Code import add_song
import sqlite3
from datetime import datetime
from dateutil import tz


def spotify_scrape(uid):
    #logs into my spotify using my app id's
    #the redirect uri is the webport that is opened that allows the user to give permission to the app to access their spotify
    #the scope allows the app to read the users recently played songs
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="36ba86b4561841d3adb38418d2ed91dc",
                                                   client_secret="07835964e1e54220aa5d29881603958d",
                                                   redirect_uri="http://127.0.0.1:9090",
                                                   scope="user-read-recently-played"))

    # user = sp.user('1231448443')
    # print(user)
    spotify_list = [] #the recently played songs will be appended to this list
    songs = sp.current_user_recently_played(limit=50) #triggers the spotipy command to read the users recently played tracks
    for i, song in enumerate(songs['items']): #enumerates the song list
        spotify_list.insert(0,((song['track']['name'],song['track']['artists'][0]['name'],song['track']['album']['name'],song['track']['duration_ms'],song['played_at'])))
        #always inserts at position 0 this means the most recently played track will be added last
        #song['track']['name'] code to get song name
        #(song['track']['artists'][0]['name']) code to get artist name
        #(song['track']['album']['name']) code to get album name
        #(song['track']['duration_ms']) code to get song duration
        #song['played_at'] code to get play date and time


    def Duration_MS_to_MINSECS(ms): #converts the track length from milliseconds to mm:ss format
        min = ms // 60000 #calculates the minute value
        sec = (ms - min * 60000) // 1000 #removes only the minute value and calculates the seconds value from the remaining time
        if len(str(sec)) < 2: #adds the leading 0 to single digit numbers for storage
            sec = '0' + str(sec)
            duration = str(min) + ':' + sec #joins the minutes and seconds into one string
        else: #joins the minutes and seconds into one string
            duration = str(min) + ":" + str(sec)
        return duration #returns the duration so it can be used later in the code

    def Date_Time_Separate(dt): #separates the Spotify date and time format ('2021-05-21T22:39:36.218Z')
        # first converts the spotify time (UTC) to local time
        d = (dt.split('T')[0])  # splits at the T and returns only the first value (the date)
        t0 = dt.split('T')[1]  # returns the second half of the T split
        t1 = t0.split(':')[0], t0.split(':')[1]  # splits at : and returns only the first and second values (mm,ss)
        time_split = ':'.join(t1)  # joins the list into string mm:ss
        dt2 = d + ' ' + time_split #joins the 2 strings so that they can be interpreted by the utc, tz and datetime commands
        from_zone = tz.tzutc() #sets the from time as utc
        to_zone = tz.tzlocal() #sets the time zone to convert to as the local time zone
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


    def join_date_time(d,t): #creates a list of each date and time value so they can be compared
        new = []
        d1 = d.split('/') #splits date at every / divisor
        d1.reverse() #reverses the list so that it is in YYYY MM DD order
        for i in d1: #adds each element to the new list
            new.append(i)
        t1 = t.split(':') #splits time at :
        for i in t1: #appends the values to the new list
            new.append(i)
        return (new)
        #each subsequent element in the list is smaller Year Month Day Hour Minute

        #I needed 2 different code sections because the Spotify Timestamp was in a different format
    def get_latest_spotify(): #gets the current users last spotify update day/time
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
        #new_date_time list is also in Year Month Day Hour Minute

    def add_songs(spotify_list):
        songs_to_add = 0
        latest = get_latest_spotify() #returns the users latest spotify update date and time list
        # finds only the songs that have been played after the last spotify update
        for i in spotify_list: #iterates through the list of spotify songs
            #Separates the date and time values of the Spotify timestamp
            d = Date_Time_Separate(i[-1])[0]
            t = Date_Time_Separate(i[-1])[1]
            date_time = (join_date_time(d,t)) #returns the list of the current songs play time
            count = 0
            #compares the latest update date and time and the date and time of songs being added
            for t in range(0, len(date_time)):
                # loop keeps running if the values are the same
                if count < 5: #as soon as one value is greater the code will stop comparing the rest of the values
                    if int(latest[t]) < int(date_time[t]):
                        count += 5 #if any of the values are greater 5 is added to the count
                    elif int(latest[t]) > int(date_time[t]):
                        break #if any of the values are smaller breaks the loop
                    #if a value is the same then the loop compares the next values in the list


            if count == 5: #only runs if there was a greater value which increased the count
                songs_to_add += 1 #adds to the songs to add count for next code block
                length = Duration_MS_to_MINSECS(i[3]) #converts the length of the song from Milliseconds to Minutes:Seconds
                date = Date_Time_Separate(i[4])[0] #Separates the date value
                time = Date_Time_Separate(i[4])[1]#Separates the time values
                add_song(i[0],i[1],i[2],length,' ',uid,date,time, 'Spotify') #runs the add song code

        if songs_to_add != 0: #updates the users last spotify update timestamp
            last_update = datetime.now()
            conn = sqlite3.connect('MLDB.db', timeout=5)
            cursorObj = conn.cursor()
            cursorObj.execute(
                f"UPDATE User set Spotify_Last_Update = '{last_update}' where id = {uid}")
            session = cursorObj.fetchall()
            conn.commit()


    add_songs(spotify_list)

#Test Code
#Get songs
#Compare them to a set date
#Check time change function
#Check date change function
#Return in format they will be written in