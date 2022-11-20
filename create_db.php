<?php
$servername = "localhost";
$username = "username"; //will have to change this to get user input
$password = "password"; //will have to change this to get user input

// Create connection
$conn = mysqli_connect($servername, $username, $password);
// Check connection
if (!$conn) {
  die("Connection failed: " . mysqli_connect_error());
}

// Create database
$sql = "CREATE DATABASE myDB";
if (mysqli_query($conn, $sql)) {
  echo "Database created successfully";
} else {
  echo "Error creating database: " . mysqli_error($conn);
}

$sql = "CREATE TABLE Station
(
  station_ID INT NOT NULL,
  name VARCHAR(20) NOT NULL,
  location VARCHAR(20) NOT NULL,
  PRIMARY KEY (station_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table Station created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE Route
(
  route_ID INT NOT NULL,
  stops INT NOT NULL,
  PRIMARY KEY (route_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table Route created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE Track
(
  track_ID INT NOT NULL,
  direction VARCHAR(2) NOT NULL,
  PRIMARY KEY (track_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table Track created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE Schedule
(
  sched_ID INT NOT NULL,
  source INT NOT NULL,
  destination INT NOT NULL,
  start_time INT NOT NULL,
  end_time INT NOT NULL,
  PRIMARY KEY (sched_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table Schedule created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE User
(
  username VARCHAR(20) NOT NULL,
  password VARCHAR(20) NOT NULL,
  first_name VARCHAR(15) NOT NULL,
  last_name VARCHAR(15) NOT NULL,
  user_ID INT NOT NULL,
  PRIMARY KEY (user_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table User created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE track_route
(
  route_ID INT NOT NULL,
  track_ID INT NOT NULL,
  PRIMARY KEY (route_ID, track_ID),
  FOREIGN KEY (route_ID) REFERENCES Route(route_ID),
  FOREIGN KEY (track_ID) REFERENCES Track(track_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table track_route created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE sched_station
(
  station_ID INT NOT NULL,
  sched_ID INT NOT NULL,
  PRIMARY KEY (station_ID, sched_ID),
  FOREIGN KEY (station_ID) REFERENCES Station(station_ID),
  FOREIGN KEY (sched_ID) REFERENCES Schedule(sched_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table sched_station created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE route_station
(
  route_ID INT NOT NULL,
  station_ID INT NOT NULL,
  PRIMARY KEY (route_ID, station_ID),
  FOREIGN KEY (route_ID) REFERENCES Route(route_ID),
  FOREIGN KEY (station_ID) REFERENCES Station(station_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table route_station created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE Train
(
  train_ID INT NOT NULL,
  train_length INT NOT NULL,
  route_ID INT NOT NULL,
  sched_ID INT NOT NULL,
  PRIMARY KEY (train_ID),
  FOREIGN KEY (route_ID) REFERENCES Route(route_ID),
  FOREIGN KEY (sched_ID) REFERENCES Schedule(sched_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table Train created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE Cargo
(
  cargo_ID INT NOT NULL,
  type INT NOT NULL,
  weight INT NOT NULL,
  owner VARCHAR(10) NOT NULL,
  car_number INT NOT NULL,
  train_ID INT NOT NULL,
  PRIMARY KEY (cargo_ID),
  FOREIGN KEY (train_ID) REFERENCES Train(train_ID)
)";


if ($conn->query($sql) === TRUE) {
  echo "Table Cargo created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

$sql = "CREATE TABLE train_track
(
  train_ID INT NOT NULL,
  track_ID INT NOT NULL,
  PRIMARY KEY (train_ID, track_ID),
  FOREIGN KEY (train_ID) REFERENCES Train(train_ID),
  FOREIGN KEY (track_ID) REFERENCES Track(track_ID)
)";

if ($conn->query($sql) === TRUE) {
  echo "Table train_track created successfully";
} else {
  echo "Error creating table: " . $conn->error;
}

mysqli_close($conn);
?>
