<?php
define('DATABASE_NAME', '');
define('DATABASE_USER', '');
define('DATABASE_PASS', '');
define('DATABASE_HOST', '');
include_once('./PHP-MySQL-Class/class.DBPDO.php');
$DB = new DBPDO();
$ship1 = $_GET["u1"];
$ship2 = $_GET["u2"];
switch($_GET['c']){
    case 'ship' :
        if(empty($ship1) && empty($ship2)) die("WAT?");
        $DB->execute("INSERT INTO ships (username_1, username_2) VALUES ('$ship1', '$ship2')");
        echo "$ship1 x $ship2 is added.";
    break;
    case 'rship' :
        if(empty($ship1) && empty($ship2)) die("WAT?");
        $DB->fetch("DELETE FROM ships WHERE username_1='$ship1' AND username_2='$ship2'");
        echo "$ship1 x $ship2 is removed.";
        break;
    case 'random' :
    $Query = $DB->fetchAll("SELECT * FROM ships ORDER BY RAND() LIMIT 1");
    if (!$Query) {
    echo '404 ship not found.';
    }else{
      foreach ($Query as $n => $Query) {
        echo $Query['username_1'] . " x " . $Query['username_2'];
      }
    }
    break;
    default :
    $Query = $DB->fetchAll("SELECT * FROM ships");
    if (!$Query) {
    echo 'No ships?';
    }else{
    foreach ($Query as $n => $Query) {
      $i++;
      echo $i . "|" . $Query['username_1'] . " x " . $Query['username_2'] . "\n";
    }
  }
    break;
}
