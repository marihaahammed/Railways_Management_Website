<?php
/* Database credentials. */
define('DB_SERVER', 'localhost');
define('DB_USERNAME', ''); //Yaseen will fill in
define('DB_PASSWORD', ''); //Yasee will fil in
define('DB_NAME', 'user');
 
/* Attempt to connect to MySQL database */
$mysqli = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
 
// Check connection
if($mysqli === false){
    die("ERROR: Could not connect. " . $mysqli->connect_error);
}
?>