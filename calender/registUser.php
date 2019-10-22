<?php
    require_once("common.php");
    if(!isset($_POST["insert"])) {
        header("location: userregist.html");
    }

    if(!(isset($_POST["userID"])&&isset($_POST["password"]))){
        header("location: userregist.html");
    }        

    try{
        $pdo = DBConnection();
        $st = $pdo->prepare("INSERT INTO login VALUES(0,?,?)");
        
        $password = password_hash($_POST["password"], PASSWORD_DEFAULT, array('cost' => 10));

        $st->execute(array(strip_tags($_POST["userID"]),$password));

        header("location: userregist.html");
    }catch(Exception $e) {
        print("エラー：" . $e->getMessage());
    }
    