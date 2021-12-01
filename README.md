# Purpose of this database in the context of the startup, sparkify, and their analytical goals.
   
 I imagine the data collected by the songplays table which is the center of this OLAP schema, giving to the company information about how they users use their app about how their users interact with their playform, what songs they listen, how much time they listen to their music, what music they listen, where are them located, and what browser are they using. You can use this kind of information for marketing purposes, or to develop an app depending on the browser or the OS they are using.
 
 
 # State and justify your database schema design and ETL pipeline.
 
 The database schema used this time is a star schema based on the simpler queries that will be made to the database, having has the fact table the songplays in order to obtain information about how the users interact and their information like location and level of their account.
 This kind of schema is useful to get rid of the complex queries and concentrated your fire power on the metrics.