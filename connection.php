<?php
//Define some constants in this PHP code block
$servername = "localhost";
$username = ""; // Need to come back and add
$password = ""; // 
$dbname = ""; //

$conn = new mysqli($servername, $username, $password, $dbname);
 // Check connection
 if ($conn->connect_error) {
   die("Connection failed: " . $conn->connect_error);
}




