# Code for Login/Add New User pages to connect with database

import sqlite3

#checks that there is data in the database
def checkdata():
    conn = sqlite3.connect('MLDB.db')
    cursorObj = conn.cursor()
    cursorObj.execute('select * from user')
    all_rows = cursorObj.fetchall()
    return all_rows

# Checks that the entered username and password are present together in the database
def check_user(username, password):
    conn = sqlite3.connect('MLDB.db')
    cursorObj = conn.cursor()
    cursorObj.execute('select username,password from user')
    all_rows = cursorObj.fetchall()
    for user in all_rows:
        # using indexes ensures the username is matched with the username and the same with the password
        if username == user[0] and password == user[1]:
            return True


def adduser(fname, lname, uname, pword, spotify, itunes):
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    uid = len(cursorObj.execute("select * from user").fetchall()) + 1
    cursorObj.execute(f"INSERT INTO user VALUES({uid}, '{fname}', '{lname}', '{uname}', '{pword}', '{spotify}', '{itunes}')")
    cursorObj.execute("select * from user")
    user = cursorObj.fetchall()
    conn.commit()
    conn.close()
    print(user)
