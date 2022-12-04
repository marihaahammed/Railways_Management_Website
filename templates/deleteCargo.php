<?php
	$id=$_GET['train_ID'];
	include('connection.php');
	mysqli_query($conn,"DELETE FROM `Cargo` WHERE train_ID='$id'");
	header('location:/templates/indexCargo.php');
?>