import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Loads the songfile to a dataframe like form, filters by
    the desired columns the first part filters and uploads the
    song records and the second part inserts the artist records
    
    @cur: cursor object
    @filepath: the path of the json that will be read
    """
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    
    song_data = list(song_data.values)
    if song_data[0] != '' or song_data[0] != None:
        cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'name', 'location', 'latitude', 'longitude']]
    artist_data = list(artist_data.values)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Loads the json file with the log data, filters the file
    by NextSong in the page column, converts the time value to
    ms units and expands the time data to each of its columns and
    derived data like the weekday, the week of the timestamps
    
    inserts the data into tables users, time, and songplay
    
    @cur: cursor object to communicate with the db
    @filepath: the path to the data file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query('page == "NextSong"')
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')

    # convert timestamp column to datetime
    t = df['ts']
    
    # insert time data records
    time_data = [
        df['ts'].astype(str),
        df['ts'].dt.hour,
        df['ts'].dt.day,
        df['ts'].dt.week,
        df['ts'].dt.month,
        df['ts'].dt.year,
        df['ts'].dt.weekday
    ]
    column_labels = ("timestamp", "hour", "day", "week of year", "month", "year", "weekday")
    time_dict = {key:value for key, value in zip(column_labels, time_data)}
    time_df = pd.DataFrame(time_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.read_json(filepath, lines=True)
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]
    user_df = user_df.drop_duplicates()
    user_df = user_df.dropna()
    user_df['userId'] = user_df['userId'].astype(int)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, list(row))

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        if songplay_data[3]:
            cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Performs the ETL process depending on the
    file and the function given by the arguments
    
    @cur: database cursor object
    @conn: database connection object
    @filepath: the path where the json files will be searched
    @func: function that will be executed depending if the data
        is log data or song data
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """executes the functions above but first performs a connection
    to sparkify db"""
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()