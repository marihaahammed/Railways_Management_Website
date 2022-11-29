<html>
<style>
table, th, td {
  border: 2px solid black;
}
<?php
//Define some constants in this PHP code block
$servername = "localhost";
$username = ""; // Need to come back and add
$password = ""; // 
$dbname = ""; //
?>


</style
<body>
<p><h2>Train Schedule Directory:</h2></p>
<form action="schedule-search.php" method=get>
	Enter schedule ID: <input type=text size=20 name="name">
    <p> <input type=submit value="submit">
            <input type="hidden" name="form_submitted" value="1" >
</form>


<?php //starting php code again!
if (!isset($_GET["form_submitted"]))
{
		echo "Please enter a schedule ID number and submit.";
}
else {
// Create connection

 $conn = new mysqli($servername, $username, $password, $dbname);
 // Check connection
 if ($conn->connect_error) {
   die("Connection failed: " . $conn->connect_error);
 }
 if (!empty($_GET["name"]))
 {
   $schedID = $_GET["name"]; //gets name from the form
   $sql = "SELECT sched_ID, source, destination, start_time, end_time FROM Schedule where sched_ID='$schedID'";
   $result = $conn->query($sql);
 }
 else {
	 echo "<b>Please enter a valid schedule ID number</b>";
 }
   if ($result->num_rows > 0) {
     	// Setup the table and headers
	echo "<table><tr><th>ID</th><th>Source</th><th>Destination</th><th>Departure Time:</th></tr><th>Arrival Time:</th>";
	// output data of each row into a table row
	 while($row = $result->fetch_assoc()) {
		 echo "<tr><td>".$row["sched_ID"]."</td><td>".$row["source"]."</td><td> ".$row["destination"]."</td><td>".$row["start_time"]."</td><td>".$row["end_time"]."</td></tr>";
   	}
	
	echo "</table>"; // close the table
	echo "There are ". $result->num_rows . " results.";
	// Don't render the table if no results found
   	} else {
               echo "$name not found. 0 results";
	} 
   $conn->close();
 } //end else condition where form is submitted
  ?> 
<p> 
</body>
</html>
