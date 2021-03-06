##Run The Program Through The Interface File
# Code for Login/Add New User pages to connect with databased
from datetime import datetime
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


#adds the user to the database with the entered parameters
def adduser(fname, lname, uname, pword, spotify, itunes):
    conn = sqlite3.connect('MLDB.db', timeout=5)
    cursorObj = conn.cursor()
    uid = len(cursorObj.execute("select * from user").fetchall()) + 1
    cursorObj.execute(f"INSERT INTO user VALUES({uid}, :f, :l, :u, :p, :s, '{datetime.now()}', :i, '{datetime.now()}')",{"f":fname,"l":lname,"u":uname,"p":pword,"s":spotify,"i":itunes})
    cursorObj.execute("select * from user")
    user = cursorObj.fetchall()
    conn.commit()
    conn.close()
    print(user)
