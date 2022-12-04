<?php
	include('connection.php');
	$id=$_GET['train_ID'];
 
	
	$type=$_POST['type'];
	$weight=$_POST['weight'];
    $owner=$_POST['owner'];
    $carNumber=$_POST['car_number'];
    $trainID=$_POST['train_ID'];

 
	mysqli_query($conn,"UPDATE `Cargo` SET type='$type', weight='$weight', owner='$owner', car_number ='$carNumber', train_ID='$trainID where train_ID='$id'");
	header('location:/templates/indexCargo.php');
?>
