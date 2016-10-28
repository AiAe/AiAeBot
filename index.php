<?php
define('DATABASE_NAME', '');
define('DATABASE_USER', '');
define('DATABASE_PASS', '');
define('DATABASE_HOST', '');
include_once('./libs/class.DBPDO.php');
$DB = new DBPDO();
$ship1 = $_GET["u1"];
$ship2 = $_GET["u2"];
switch($_GET['c']){
    case 'ship' :
        if(empty($ship1) && empty($ship2)) die("WAT?");
        $checker = $DB->fetch("SELECT * FROM ships WHERE username_1='$ship1' AND username_2='$ship2'");
        if($checker) die("Ship exists in database!.");
        $checker = $DB->fetch("SELECT * FROM ships WHERE username_1='$ship2' AND username_2='$ship1'");
        if($checker) die("Ship exists in database!.");
        $DB->execute("INSERT INTO ships (username_1, username_2) VALUES ('$ship1', '$ship2')");
        echo "$ship1 x $ship2 is added.";
    break;
    case 'rship' :
        if(empty($ship1) && empty($ship2)) die("WAT?");
        $checker = $DB->fetch("SELECT * FROM ships WHERE username_1='$ship1' AND username_2='$ship2'");
        if(!$checker) die("404 ship not found.");
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
                $find1 = strpos($Query['username_1'], ":");
                $find2 = strpos($Query['username_2'], ":");
                $marge = $Query['username_1'] . " x " . $Query['username_2'];
                $remove_ids = explode(":", $marge);
                echo $i . "| ";
                if($find1 == true && $find2 == true){
                    echo $remove_ids[1] . " x " . $remove_ids[3] . "\n";
                }elseif($find1 == false && $find2 == false){
                    echo $marge . "\n";
                }elseif($find1 == true && $find2 == false){
                    echo $remove_ids[1] . " x " . $Query['username_2'] . "\n";
                }elseif($find1 == false && $find2 == true){
                    echo $Query['username_1'] . " x " . $remove_ids[1] . "\n";
                }
            }
        }
    break;
}
