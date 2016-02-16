<?php

$con = mysql_connect("localhost","root", PASSWORD);

if (!$con) {
die('Could not connect: ' . mysql_error());
}

mysql_select_db("thesis", $con);
$time = $_GET["time"];
$date = new DateTime($time);
//echo $date->format('Y-m-d H:i:s');
//$date = date('Y-m-d H:i:s', time());
//echo $date;
//date_add($date,date_interval_create_from_date_string("40 days"));
//echo date_format($date,"Y-m-d H:i:s");
//echo "-----";

$result = mysql_query("SELECT * FROM `power`") or die ("Error");

while($row = mysql_fetch_array($result)){
	$temp= new DateTime($row['datetime']);
	//$view= $temp->format('Y-m-d H:i:s');
	$view= $temp->format('U');
	//echo $temp->format('Y-m-d H:i:s');
	if ($temp>$date){
		//echo $row['datetime'] . "/" . $row['sensor_value']. "/" ;
		echo $view . "/" . $row['sensor_id'] . "/" . $row['sensor_value']. "/" ;
	}
}

mysql_close($con);
?>
