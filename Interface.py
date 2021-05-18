from tkinter import *
from Login_Access import *
from Main_Code import *
from Stat_Windows import *
from Update_Windows import *
# Code for the login section
class LoginPage():
    def __init__(self, login):
        self.name = 'Login'
        self.master = login

        login.title("Log In")
        login.geometry("400x200+100+100")

        #Labels for the entry fields
        login.namelabel = Label(login, text="Name =")
        login.namelabel.grid(row=0, column=0)

        login.unamelabel = Label(login, text="Username =")
        login.unamelabel.grid(row=1, column=0)

        login.pwordlabel = Label(login, text="Password =")
        login.pwordlabel.grid(row=2, column=0)

        #Login entry fields
        login.name = Entry(login)
        login.name.grid(row=0, column=1)
        login.name.insert(0, 'Tom Gallagher')

        login.uname = Entry(login)
        login.uname.grid(row=1, column=1)
        login.uname.insert(1, 'Tom1998')

        login.pword = Entry(login)
        login.pword.grid(row=2, column=1)
        login.pword.insert(2, 'QWERTY1234')

        #Runs the open main window command when pressed
        login.LoginButton = Button(login, text="Log In", command=lambda: self.open_main_window(login))
        login.LoginButton.grid(row=3, column=1)

        #Runs the open new User window comman when pressed
        login.CreateAccount = Button(login, text="Create New Account", command=lambda: self.open_newUser_window(login))
        login.CreateAccount.grid(row=5, column=1)

    def open_main_window(self,login):
        x = login.name.get() #Display name for the session
        y = login.uname.get()#Username
        z = login.pword.get()#Password
        if len(checkdata()) < 1:
            label3 = Label(login, text="If you do not have an account \n you can create on below")
            label3.grid(row=3, column=3)
            return 'done'

        #Takes the entered username and password and runs the check_user command from the Login Access code
        #If there is a match the program opens the main page and stores the username and display name and kills the login page
        if check_user(y,z) == True:
            root = Tk()
            MainPage(root, x, y)
            login.destroy()
            print(z)
        #If there is no match an error message is displayed
        else:
            label3 = Label(login, text="Incorrect Name or Password entered")
            label3.grid(row=2, column=3)
            label3 = Label(login, text="If you do not have an account \n you can create on below")
            label3.grid(row=3, column=3)


    def open_newUser_window(self,login):
        #Opens a window to allow the user to create an account
        New_User = Tk()
        New_User.title("Create New Account")
        New_User.geometry("400x200+100+100")

        #Labels for all the entry fields
        f_name = Label(New_User, text="Name =")
        f_name.grid(row=0, column=0)

        s_name = Label(New_User, text="Surname =")
        s_name.grid(row=1, column=0)

        u_name = Label(New_User, text="Username =")
        u_name.grid(row=2, column=0)

        pword = Label(New_User, text="Password =")
        pword.grid(row=3, column=0)

        spotify = Label(New_User, text="Spotify Details =")
        spotify.grid(row=4, column=0)

        itunes = Label(New_User, text="iTunes Details =")
        itunes.grid(row=5, column=0)

        #Entry Field codes
        f_name_entry = Entry(New_User)
        f_name_entry.grid(row=0, column=1)
        f_name_entry.insert(0, 'Firstname(s)')

        s_name_entry = Entry(New_User)
        s_name_entry.grid(row=1, column=1)
        s_name_entry.insert(1, 'Lastname(s)')

        u_name_entry = Entry(New_User)
        u_name_entry.grid(row=2, column=1)
        u_name_entry.insert(2, 'Username')

        pword_entry = Entry(New_User)
        pword_entry.grid(row=3, column=1)
        pword_entry.insert(3, 'Password')

        spotify_entry = Entry(New_User)
        spotify_entry.grid(row=4, column=1)
        spotify_entry.insert(4, 'Spotify')

        itunes_entry = Entry(New_User)
        itunes_entry.grid(row=5, column=1)
        itunes_entry.insert(5, 'iTunes')

        def createuser(): #function for the create user button
            fname = f_name_entry.get()
            lname = s_name_entry.get()
            uname = u_name_entry.get()
            pword = pword_entry.get()
            spotify = spotify_entry.get()
            itunes = itunes_entry.get()
            for user in checkdata(): #runs the check user command in Login_Access to ensure username is unique
                if uname in user:
                    label6 = Label(New_User, text="Username already in user \n please enter a unique username")
                    label6.grid(row=3, column=3)
                    return
            #creates a user with all the data gathered from the filled in forms
            adduser(fname,lname,uname,pword,spotify,itunes)
            New_User.destroy()
        #button that executes the create user command
        CreateAccount = Button(New_User, text="Create New Account", command=lambda: createuser())
        CreateAccount.grid(row=7, column=1)


class MainPage():
    def __init__(self, main, user, username):
        self.name = 'main'
        self.master = main
        self.user = user
        self.username = username
        self.user_id = get_user_id(username)

        main.title("Main Page")
        main.geometry("400x275+100+100")


        #Headings Code ADD TEXT FORMATTING
        main.label = Label(main, text='Music Listening Database')
        main.label.grid(row=1, column=1, columnspan = 5, pady=(5,5))

        main.name = Label(main, text = user)
        main.name.grid(row = 2, column = 5, sticky='w')

        main.total_time = Label(main, text=f'Total listening time: {get_time(self.user_id)}')
        main.total_time.grid(row = 3, column = 1, columnspan = 2, sticky='w')

        main.total_songs = Label(main, text= f'Total Songs: {song_count(self.user_id)}')
        main.total_songs.grid(row = 3, column = 5,sticky='w')


        #Interactions Code
        #Songs Interactions
        main.songs = Label(main, text='Songs')
        main.songs.grid(row=4, column=1,sticky='w', pady=(5,5))

        Music_Stats = Button(main, text="Stats", command = lambda:self.open_stats_window('music'))
        Music_Stats.grid(row=4, column=2,pady=(5,5))

        Music_Update = Button(main, text="Update")
        Music_Update.grid(row=4, column=3,pady=(5,5))

        #Artist Interactions
        main.artist = Label(main, text='Artist')
        main.artist.grid(row=5, column=1, sticky='w', pady=(5,5))

        Artist_Stats = Button(main, text="Stats", command = lambda:self.open_stats_window('artist'))
        Artist_Stats.grid(row=5, column=2)

        Artist_Update = Button(main, text="Update")
        Artist_Update.grid(row=5, column=3)

        #Album interactions
        main.album = Label(main, text='Album')
        main.album.grid(row=6, column=1, sticky='w',pady=(5,5))

        Album_Stats = Button(main, text="Stats", command = lambda:self.open_stats_window('album'))
        Album_Stats.grid(row=6, column=2)

        Album_Update = Button(main, text="Update")
        Album_Update.grid(row=6, column=3)

        #Source (Spotify, itunes, other) interactions
        main.source = Label(main, text='Source')
        main.source.grid(row=7, column=1, sticky='w',pady=(5,5))

        Source_Stats = Button(main, text="Stats", command = lambda:self.open_stats_window('source'))
        Source_Stats.grid(row=7, column=2)

        Source_Update = Button(main, text="Update")
        Source_Update.grid(row=7, column=3)

        #Session (Study, Party, Relaxing etc) Code
        main.session = Label(main, text='Session')
        main.session.grid(row=8, column=1, sticky='w',pady=(5,5))

        Session_Stats = Button(main, text="Stats", command = lambda:self.open_stats_window('session'))
        Session_Stats.grid(row=8, column=2)

        Session_Update = Button(main, text="Update")
        Session_Update.grid(row=8, column=3)

        Add_Playlist = Button(main, text="Add Playlist", command = lambda:self.open_update_window('playlist'))
        Add_Playlist.grid(row=9, column=2, columnspan = 2,pady=(5,5))

    def open_stats_window(self, type):
        if type == 'music':
            song_details = (music_stats(self.user_id))
            song = song_details[0]
            plays = song_details[1]
            artist = song_details[2]
            root = Tk()
            Song_Stat_Window(root, song, plays, artist)
        print (type)
        if type == 'artist':
            artist_details = (artist_stats(self.user_id))
            artist = artist_details[0]
            times = artist_details[1]
            song = artist_details[2]
            root = Tk()
            Artist_Stats_Window(root, artist, times, song)
        if type == 'album':
            album_details = (album_stats(self.user_id))
            album = album_details[0]
            artist = album_details[1]
            song = album_details[2]
            root = Tk()
            Album_Stats_Window(root, album, artist, song)
        if type == 'source':
            source_details = (source_stats(self.user_id))
            source = source_details[0]
            song = source_details[1]
            root = Tk()
            Source_Details(root,source,song)
        if type == 'session':
            session_details = (session_stats(self.user_id))
            session = session_details[0]
            song = session_details[1]
            root = Tk()
            Session_Details(root, session, song)


    def open_update_window(self, type):
        if type == 'playlist':
            root = Tk()
            Playlist(root,self.user_id)



root = Tk()
LoginPage(root)
root.mainloop()