<?php
    session_start();
    require_once("common.php");

    if(!isset($_POST["userid"])||!isset($_POST["password"])){
        header("location: login.html");
    }
    if(empty($_POST["userid"])||empty($_POST["password"])){
        header("location: login.html");
    }
    try{
        $pdo = DBConnection();
        $st = $pdo->prepare("SELECT * FROM login WHERE name=?");
        $jumpPage = "location: login.html";

        $name = $_POST["userid"];
        $password = $_POST["password"];

        $st->execute(array($name));

        while($row = $st->fetch()){
            print($row["password"]);
            if(($name == $row["name"]) && (password_verify($password, $row["password"]))){
                session_regenerate_id(true);
                $_SESSION["name"] = $row['name'];

                $jumpPage="location: calender.html";
            }
        }
        header($jumpPage);
    }catch(Exception $e) {
        header("location: login.html");
    }