<?php
//Define some constants in this PHP code block
$servername = "localhost";
$username = "yshaikh"; // Need to come back and add
$password = "dJTy7cg2"; // 
$dbname = "user"; //

$conn = new mysqli($servername, $username, $password, $dbname);
 // Check connection
 if ($conn->connect_error) {
   die("Connection failed: " . $conn->connect_error);
}




