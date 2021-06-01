import pytest

from Main_Code import *
from test_samples import *
from Update_Windows import *

# some functions were written within functions so I could not directly test them
# so I created a samples file of the code I needed to test
# Testing was mainly done on code pieces that users could interact with


#Main Code Tests
@pytest.fixture
def user1():
    u_name = 'tom1234g'
    p_word = 'password'
    u_id = 2
    return u_name, p_word, u_id


@pytest.fixture
def song():
    title = 'Untitled'
    artist = 'Unnamed'
    album = 'Untitled'
    length = ':::'
    genre = 'No-Noise'
    userid = 1
    return title,artist,album,length,genre,userid


@pytest.fixture
def lengths():
    length1 = ' '
    length2 = '12:12'
    length3 = '.3'
    return length1,length2,length3


@pytest.fixture
def dates():
    date1 = '12/11/2021'
    date2 = '12/12/12/12'
    date3 = '12:12'
    return date1,date2,date3


@pytest.fixture
def times():
    time1 = '25:00'
    time2 = '12/21/12'
    time3 = '12:12'
    return time1,time2,time3


def test_userid(user1):  # tests base access to the database
    assert (get_user_id(user1[0]) == 1)


def test_length(lengths):  # tests that the lengths formats of songs are standardized
    assert check_formats(length=lengths[0]) == '3:30'
    assert check_formats(length=lengths[1]) == '12:12'
    assert check_formats(length=lengths[2]) == '3:30'


def test_dates(dates):  # tests that the dates are all standardized
    assert check_formats(date1=dates[0]) == '12/11/2021'
    assert check_formats(date1=dates[1]) != '12/12/12/12'
    assert check_formats(date1=dates[2]) != '12:12'


def test_times(times):  #checks that the times are standardized
    assert check_formats(time1=times[0]) != '25:00'
    assert check_formats(time1=times[1]) != '12/21/12'
    assert check_formats(time1=times[2]) == '12:12'


def test_get_time(user1):
    assert (song_count(user1[2]) > 0)
# def test_add_song(song): #Only used initially.
#     assert (add_song(song[0],song[1],song[2],song[3],song[4],song[5]) == 'Yes')


# Login Tests
@pytest.fixture
def new_users():
    user1 = ['tomg','1234']
    user2 = ['tom1234g','password']
    user3 = ['Tom1234', 'Password']
    return user1,user2,user3


def test_check_user(new_users):
    user1 = new_users[0]
    user2 = new_users[1]
    user3 = new_users[2]
    assert (check_user(user1[0],user1[1]) != True)
    assert (check_user(user2[0], user2[1]) == True)
    assert (check_user(user3[0], user3[1]) == True)


# Spotify Tests
@pytest.fixture
def milliseconds():
    milliseconds = [11111222,2424242,12302032,1]
    return milliseconds


# checks that the spotify times are converted correctly to mm:ss
def test_ms_to_minsecs(milliseconds):
    time1 = milliseconds[0]
    time2 = milliseconds[1]
    time3 = milliseconds[2]
    time4 = milliseconds[3]
    assert (Duration_MS_to_MINSECS(time1) == '185:11')
    assert (Duration_MS_to_MINSECS(time2) == '40:24')
    assert (Duration_MS_to_MINSECS(time3)=='205:02')
    assert (Duration_MS_to_MINSECS(time4)== '0:00')


@pytest.fixture
def datetimes():
    datetime=['2021-05-21T22:39:36.218Z','2021-05-21T22:39:36','2021-05-21T22:39']
    return datetime


# checks that the date time separate function works
def test_dt_separate(datetimes):
    date1 = datetimes[0]
    date2 = datetimes[1]
    date3 = datetimes[2]
    assert Date_Time_Separate(date1) == ('22/05/2021', '00:39')
    assert len(Date_Time_Separate(date1)) == 2
    assert Date_Time_Separate(date2) == ('22/05/2021', '00:39')
    assert Date_Time_Separate(date3) == ('22/05/2021', '00:39')


@pytest.fixture
def datetimes2():
    datetime = ['22/05/2021', '00:39']
    return datetime


# tests that the separated date times can be joined correctly
def test_dt_join(datetimes2):
    dt1 = datetimes2
    assert join_date_time(dt1[0],dt1[1]) == ['2021','05','22','00','39']


# checks that when the users latest spotify update is returned it contains 5 values
# and that the 1st value is 4 characters, which means the year is returned correctly
def test_latest_spotify(user1):
    assert len(get_latest_spotify(user1[2])) == 5
    assert len(get_latest_spotify(user1[2])[0]) == 4


#iTunes Tests
@pytest.fixture
def update_dates():
    Date1 = ['2021', '05', '01', '12', '15']
    Date2 = ['2021', '06', '01', '12', '15']
    Date3 = ['2021', '07', '01', '12', '15']
    return Date1, Date2, Date3


# checks the get file function,
# the check latest update
# and the join date time function from the itunes code
def test_get_file(update_dates):
    assert get_file(2, update_dates[0])[0] == 10
    assert get_file(2, update_dates[1])[0] == 3
    assert get_file(2, update_dates[2])[0] == 0
    # checks that there is data in all indexes
    for song in get_file(2, update_dates[0])[1]:
        for i in song:
            assert i != ''




