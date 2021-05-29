import sqlite3

def create_database():
    conn= sqlite3.connect('MLDB.db')
    cursorObj= conn.cursor()
    cursorObj.execute("""CREATE TABLE User(id integer PRIMARY KEY,
                      first_name text,
                      last_name text,
                      username UNIQUE,
                      password text,
                      Spotify text,
                      Spotify_Last_Update text,
                      iTunes text,
                      iTunes_Last_Update text)""")
    # conn.commit()
    cursorObj.execute("""CREATE TABLE Song(id integer PRIMARY KEY,
                      Title text,
                      Artist text,
                      Album text,
                      Length text,
                      Genre text)""")
    # conn.commit()
    cursorObj.execute("""CREATE TABLE Plays(id integer PRIMARY KEY,
                      Song integer,
                      Source text,
                      Date text,
                      Time text,
                      Session text,
                      User_ID integer,
                      itunes_Base_Plays integer,
                      FOREIGN KEY(Song) references Song(id) on delete set null
                      FOREIGN KEY(User_ID) references User(id) on delete set null)""")
    conn.commit()




