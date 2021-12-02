# Purpose of this database in the context of the startup, sparkify, and their analytical goals.
   
 I imagine the data collected by the songplays table which is the center of this OLAP schema, giving to the company information about how they users use their app about how their users interact with their playform, what songs they listen, how much time they listen to their music, what music they listen, where are them located, and what browser are they using. You can use this kind of information for marketing purposes, or to develop an app depending on the browser or the OS they are using.
 
 
 # State and justify your database schema design and ETL pipeline.
 
 The database schema used this time is a star schema based on the simpler queries that will be made to the database, having has the fact table the songplays in order to obtain information about how the users interact and their information like location and level of their account.
 This kind of schema is useful to get rid of the complex queries and concentrated your fire power on the metrics.
 
 # Database Shema
 The schema chosen today is the star schema for easier sql statements.
 
 The star schema is divided by two parts: The fact table and the dimension tables
 
 #### Fact table:
 1. Songplays: Which are the records in log data associates with song plays.
 * songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
 
 #### Dimension tables:
 2. Users
 * user_id, first_name, last_name, gender, level
 3. Songs
 * song_id, title, artist_id, year, duration
 4. Artists
 * artist_id, name, location, latitude, longitude
 5. Time: Timestamps of records in songplays broken down into specific units
 * start_time, hour, day, week, month, year, weekday
 
 # How to run the python scripts
 To run the scripts first open a terminal, then perform the next commands:
 * python create_tables.py
 * python elt.py
 
 # Explanation of the files
 #### data
 The folder with log and song data files
 #### create_tables.py
 The python script that imports the psycopg2 module, connects to the database, imports the sql queries from sql_queries.py and creates the tables needed for the project, it also drops the tables.
 #### etl.ipynb
 Is a file that let you see a quick review of what is done in etl.py, but with explanations in markdown thanks to jupyter notebook.
 #### sql_queries.py
 Well this one is easy, it has in the actual sql statements that create tables, drop and insert data.
 #### test.ipynb
 This one let's you check if the tables you have created or the date you have inserted were inserted or created succesfully.