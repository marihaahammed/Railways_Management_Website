import mysql.connector

db = mysql.connect("database.db")

cursor = db.cursor()

cursor.execute("CREATE DATABASE myDB")

#with initial setup out of the way, we can now create the contents of the database
#this .py file was created as a preferred way of creating and filling the database instead of a .php file
#that way, we can run it once and the database will have been created. 


	cursor.execute('DROP TABLE IF EXISTS Station')
	cursor.execute('DROP TABLE IF EXISTS Route')
	cursor.execute('DROP TABLE IF EXISTS Track')
	cursor.execute('DROP TABLE IF EXISTS Schedule')
	cursor.execute('DROP TABLE IF EXISTS User')
	cursor.execute('DROP TABLE IF EXISTS track_route')
	cursor.execute('DROP TABLE IF EXISTS sched_station')
	cursor.execute('DROP TABLE IF EXISTS route_station')
	cursor.execute('DROP TABLE IF EXISTS Train')
	cursor.execute('DROP TABLE IF EXISTS Cargo')
	cursor.execute('DROP TABLE IF EXISTS train_track')
	

	cursor.execute('''
		
		CREATE TABLE Station
		(
			station_ID INT NOT NULL,
  			name VARCHAR(20) NOT NULL,
  			location VARCHAR(20) NOT NULL,
  			PRIMARY KEY (station_ID)
		)
	''')

	cursor.execute('''
		CREATE TABLE Route
		(
  			route_ID INT NOT NULL,
  			stops INT NOT NULL,
			PRIMARY KEY (route_ID)
		)
	''')

	cursor.execute('''
		CREATE TABLE Track
		(
  			track_ID INT NOT NULL,
  			direction VARCHAR(2) NOT NULL,
  			PRIMARY KEY (track_ID)
		)
	''')
