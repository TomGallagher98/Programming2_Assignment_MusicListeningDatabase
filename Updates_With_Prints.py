#I added these print statements during the lesson, if you want to view them in the code
#I removed the original comments so the updates can be found easier

###iTunes - Run iTunes Scrape
def write_to_db(songs):
    for song in songs:
        base = find_base_plays(song[0], uid)

        min = int(song[4]) // 60
        sec = int(song[4]) - (min * 60)
        length = str(min) + ':' + str(sec)
        dt = song[-1].split(' ')
        date = dt[0]
        time = dt[1]
        if dt[2] == 'PM':
            x = (time.split(':'))
            y = int(x[0])
            if y != 12:
                y += 12
            x[0] = str(y)
            time = ':'.join(x)
        if base[0] == 0:
            add_song(song[0], song[1], song[2], length, song[3], 2, date, time, 'iTunes', song[5])
            print(song[0], song[1], song[2], length, song[3], 2, date, time, 'iTunes', song[5]) ############ADDED PRINT STATEMENT
        else:
            plays = int(song[5]) - (int(base[0]) + int(base[1]) - 1)
            for i in range(0, plays):
                add_song(song[0], song[1], song[2], length, song[3], 2, date, time, 'iTunes')
                print(song[0], song[1], song[2], length, song[3], 2, date, time, 'iTunes') ############ADDED PRINT STATEMENT


##SPOTIFY - Spotify scrape
    for i, song in enumerate(songs['items']):
        print(song) ######ADDED PRINT STATEMENT
        spotify_list.insert(0, ((
        song['track']['name'], song['track']['artists'][0]['name'], song['track']['album']['name'],

        song['track']['duration_ms'], song['played_at'])))

    def add_songs(spotify_list):
        songs_to_add = 0
        latest = get_latest_spotify()
        for i in spotify_list:
            d = Date_Time_Separate(i[-1])[0]
            t = Date_Time_Separate(i[-1])[1]
            date_time = (join_date_time(d,t))
            count = 0

            for t in range(0, len(date_time)):
                # loop keeps running if the values are the same
                if count < 5:
                    if int(latest[t]) < int(date_time[t]):
                        count += 5
                    elif int(latest[t]) > int(date_time[t]):
                        break


            if count == 5:
                songs_to_add += 1
                length = Duration_MS_to_MINSECS(i[3])
                date = Date_Time_Separate(i[4])[0]
                time = Date_Time_Separate(i[4])[1]
                print(i[0],i[1],i[2],length,uid,date,time,'Spotify') ##########ADDED PRINT STATEMENT
                add_song(i[0],i[1],i[2],length,' ',uid,date,time, 'Spotify')

# Update Windows - Playlist Class - Add Playlist
        def add_playlist():
            if self.length == int(entry1.get()):
                for i in self.list:
                    if i.date == '':
                        i.date = None

                    if i.time == '':
                        i.time = None

                    x = check_song(f'{i.title}',f'{i.artist}',f'{i.album}')
                    if check_song(f'{i.title}',f'{i.artist}',f'{i.album}') is not None:
                        add_play(x,self.user,i.source,i.date,i.time,i.session)

                        print (i.title) ###########ADDED PRINT STATEMENT
                        print (i.title,i.album,i.album,i.source,i.date,i.time,i.session) ###########ADDED PRINT STATEMENT
                    else:
                        add_song(i.title,i.artist,i.album,i.t_length,'',user)
                        x = check_song(f'{i.title}', f'{i.artist}', f'{i.album}')
                        append_play(x,i.source,i.session)
                        print(i.title, i.album, i.album, i.source, i.date, i.time, i.session) ###########ADDED PRINT STATEMENT
                self.list = []
                self.length = 0
                length = Label(playlist, text=f'Current length {self.length}')
                length.grid(row=11, column=0)
            else:
               
                messagebox.showerror('Length Error', f'Error:\n Specified length and current length of playlist do not match\n Please add more songs or change specified track length')
                print ('no')