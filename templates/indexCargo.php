<!DOCTYPE html>
<html>
<head>
<title>Basic MySQLi Commands</title>
</head>
<body>
	<div>
		<form method="POST" action="addCargo.php">
			<label>Train ID:</label><input type="text" name="train_ID">
			<input type="submit" name="add">
		</form>
	</div>
	<br>
	<div>
		<table border="1">
			<thead>
				<th>Train ID</th>
				<th></th>
			</thead>
			<tbody>
				<?php
                    sesstion_start();
					include('connection.php');
					$query=mysqli_query($conn,"SELECT * FROM 'Cargo'");
                    if(isset($_SESSION['loggedin']) && $_SESSION['role_ID']>=1){
					    while($row=mysqli_fetch_array($query)){
						    ?>
						    <tr>
							    <td><?php echo $row['type']; ?></td>
							    <td><?php echo $row['weight']; ?></td>
                                <td><?php echo $row['owner']; ?></td>
                                <td><?php echo $row['car_number']; ?></td>
                                <td><?php echo $row['train_ID']; ?></td>
							    <td>
								    <a href="editCargo.php?id=<?php echo $row['userid']; ?>">Edit</a>
								    <a href="deleteCargo.php?id=<?php echo $row['userid']; ?>">Delete</a>
							    </td>
						    </tr>
                    
						    <?php
					    }
                    }elseif(isset($_SESSION['loggedin']) && $_SESSION['role_ID'] == 0){
                        echo "Access Denied";
                        die(); 
                    }
				?>
			</tbody>
		</table>
	</div>
</body>
</html>