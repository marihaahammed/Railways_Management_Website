<?php
	include('connection.php');
 
	$type=$_POST['type'];
	$weight=$_POST['weight'];
    $owner=$_POST['owner'];
    $carNumber=$_POST['car_number'];
    $trainID=$_POST['train_ID'];
 
	mysqli_query($conn,"INSERT INTO 'Cargo' (type,weight,owner,car_number,train_ID) values ('$type','$weight','$owner','$carNumber','$trainID')");
	header('location:indexCargo.php');
 
?>