import mysql.connector

db = mysql.connector.connect(
host = "localhost",
user = "yshaikh",
password = "kaddu513"
)

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

cursor.execute('''
	CREATE TABLE Schedule
	(
		sched_ID INT NOT NULL,
		source INT NOT NULL,
		destination INT NOT NULL,
		start_time INT NOT NULL,
		end_time INT NOT NULL,
		PRIMARY KEY (sched_ID)
	)
''')

cursor.execute('''
	CREATE TABLE User
	(
		username VARCHAR(20) NOT NULL,
		password VARCHAR(20) NOT NULL,
		first_name VARCHAR(15) NOT NULL,
		last_name VARCHAR(15) NOT NULL,
		user_ID INT NOT NULL,
		role_ID INT NOT NULL,
		PRIMARY KEY (user_ID)
	)
''')

cursor.execute('''
	CREATE TABLE track_route
	(
		route_ID INT NOT NULL,
		track_ID INT NOT NULL,
		PRIMARY KEY (route_ID, track_ID),
		FOREIGN KEY (route_ID) REFERENCES Route(route_ID),
		FOREIGN KEY (track_ID) REFERENCES Track(track_ID)
	)
''')

cursor.execute('''
	CREATE TABLE sched_station
	(
		station_ID INT NOT NULL,
		sched_ID INT NOT NULL,
		PRIMARY KEY (station_ID, sched_ID),
		FOREIGN KEY (station_ID) REFERENCES Station(station_ID),
		FOREIGN KEY (sched_ID) REFERENCES Schedule(sched_ID)
	)
''')

cursor.execute('''
	CREATE TABLE route_station
	(
		route_ID INT NOT NULL,
		station_ID INT NOT NULL,
		PRIMARY KEY (route_ID, station_ID),
		FOREIGN KEY (route_ID) REFERENCES Route(route_ID),
		FOREIGN KEY (station_ID) REFERENCES Station(station_ID)
	)
''')

cursor.execute('''
	CREATE TABLE Train
	(
		train_ID INT NOT NULL,
		train_length INT NOT NULL,
		route_ID INT NOT NULL,
		sched_ID INT NOT NULL,
		PRIMARY KEY (train_ID),
		FOREIGN KEY (route_ID) REFERENCES Route(route_ID),
		FOREIGN KEY (sched_ID) REFERENCES Schedule(sched_ID)
	)
''')

cursor.execute('''
	CREATE TABLE Cargo
	(
		cargo_ID INT NOT NULL,
		type INT NOT NULL,
		weight INT NOT NULL,
		owner VARCHAR(10) NOT NULL,
		car_number INT NOT NULL,
		train_ID INT NOT NULL,
		PRIMARY KEY (cargo_ID),
		FOREIGN KEY (train_ID) REFERENCES Train(train_ID)
	)
''')

cursor.execute('''
	CREATE TABLE train_track
	(
		train_ID INT NOT NULL,
		track_ID INT NOT NULL,
		PRIMARY KEY (train_ID, track_ID),
		FOREIGN KEY (train_ID) REFERENCES Train(train_ID),
		FOREIGN KEY (track_ID) REFERENCES Track(track_ID)
	)
''')

cursor.execute('''INSERT INTO User (username, password, first_name, last_name, user_ID, role_ID) VALUES ('yshaikh', 'y_pword', 'yaseen', 'shaikh', 0, 0)''')
cursor.execute('''INSERT INTO User (username, password, first_name, last_name, user_ID, role_ID) VALUES ('kpatel', 'k_pass', 'khushi', 'patel', 1, 1''')
cursor.execute('''INSERT INTO User (username, password, first_name, last_name, user_ID, role_ID) VALUES ('bgall', 'b_pass', 'brandon', 'gall', 2, 0)''')
cursor.execute('''INSERT INTO User (username, password, first_name, last_name, user_ID, role_ID) VALUES ('mahammed', 'm_pword', 'mariha', 'ahammed', 3, 1)''')
cursor.execute('''INSERT INTO User (username, password, first_name, last_name, user_ID, role_ID) VALUES ('jjoseph', 'j_pword', 'jackson', 'joseph', 4, 1)''')


connection.close()
