<?php
	include('connection.php');
	$id=$_GET['train_ID'];
	$query=mysqli_query($conn,"SELECT * FROM `Cargo` WHERE train_ID='$id'");
	$row=mysqli_fetch_array($query);
?>
<!DOCTYPE html>
<html>
<head>
<title>Basic MySQLi Commands</title>
</head>
<body>
	<h2>Edit</h2>
	<form method="POST" action="updateCargo.php?id=<?php echo $id; ?>">
		<label>Type:</label><input type="text" value="<?php echo $row['type']; ?>" name="type">
		<label>Weight:</label><input type="text" value="<?php echo $row['weight']; ?>" name="weight">
		<label>Owner:</label><input type="text" value="<?php echo $row['owner']; ?>" name="owner">
        <label>Car Number:</label><input type="text" value="<?php echo $row['car_number']; ?>" name="car_number">
        <label>Train ID:</label><input type="text" value="<?php echo $row['train_ID']; ?>" name="train_ID">
        <input type="submit" name="submit">
		<a href="index.php">Back</a>
	</form>
</body>
</html>