from tkinter import *
import tkinter.font as fnt
from DB_EX import *
from Login_Access import *


root = Tk()
main_window = root
main_window.title("Music Listening Database")
main_window.geometry("400x200+100+100")
main_window.withdraw()


def open_main_window():
    x = entry1.get()
    y = entry2.get()
    z = entry3.get()
    if len(DB.users) < 1:
        label3 = Label(login, text="If you do not have an account \n you can create on below")
        label3.grid(row=3, column=3)
        return 'done'

    for i in retDB(DB):
        if i.f == str(x) and i.l == str(y) and i.p == str(z):
            # main_window = Tk()
            # main_window.title("Music Listening Database")
            # main_window.geometry("400x200+100+100")
            main_window.deiconify()

            label = Label(main_window, text=x)
            label.grid(row=0, column=0)
            label = Label(main_window, text=y)
            label.grid(row=0, column=1)

            login.destroy()
            print(z)

            mainloop()
        else:
            label3 = Label(login, text="Incorrect Name or Password entered")
            label3.grid(row=2, column=3)
            label3 = Label(login, text="If you do not have an account \n you can create on below")
            label3.grid(row=3, column=3)


def open_newUser_window():
    New_User = Tk()
    New_User.title("Create New Account")
    New_User.geometry("400x200+100+100")

    label = Label(New_User, text="Name =")
    label.grid(row=0, column=0)

    label1 = Label(New_User, text="Surname =")
    label1.grid(row=1, column=0)

    label1 = Label(New_User, text="Password =")
    label1.grid(row=2, column=0)

    entry1 = Entry(New_User)
    entry1.grid(row=0, column=1)
    entry1.insert(0, 'Tom')

    entry2 = Entry(New_User)
    entry2.grid(row=1, column=1)
    entry2.insert(1, 'Gallagher')

    entry3 = Entry(New_User)
    entry3.grid(row=2, column=1)
    entry3.insert(2, 'QWERTY1234')
    x = entry1.get()
    y = entry2.get()
    z = entry3.get()

    CreateAccount = Button(New_User, text="Create New Account",
                           command=lambda: [createUser(x, y, z), New_User.destroy()])
    CreateAccount.grid(row=5, column=1)

    # login.destroy()
    mainloop()


def createUser(x, y, z):
    x = User(x, y, z)
    DB.adduser(x)
    print(DB.users[0].f)
    # New_User.destroy()


login = Tk()
login.title("Log In")
login.geometry("400x200+100+100")

label = Label(login, text="Name =")
label.grid(row=0, column=0)

label1 = Label(login, text="Surname =")
label1.grid(row=1, column=0)

label1 = Label(login, text="Password =")
label1.grid(row=2, column=0)

entry1 = Entry(login)
entry1.grid(row=0, column=1)
entry1.insert(0, 'Tom')

entry2 = Entry(login)
entry2.grid(row=1, column=1)
entry2.insert(1, 'Gallagher')

entry3 = Entry(login)
entry3.grid(row=2, column=1)
entry3.insert(2, 'QWERTY1234')

LoginButton = Button(login, text="Log In", command=lambda: open_main_window())
LoginButton.grid(row=3, column=1)

CreateAccount = Button(login, text="Create New Account", command=lambda: open_newUser_window())
CreateAccount.grid(row=5, column=1)

mainloop()