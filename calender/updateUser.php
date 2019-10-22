<?php
    require_once("common.php");

    if(isset($_POST["update"])){
        if(!(isset($_POST["userID"])&&isset($_POST["password"])&&isset($_POST["userIDhidden"])&&isset($_POST["ID"]))){
            header("location: userregist.html");
        }
    } elseif (isset($_POST["delete"])) {
        if(!isset($_POST["userIDhidden"])){
            header("location: userregist.html");
        }
    } else {
        header("location: userregist.html");
    }

    try{
        $pdo = DBConnection();

        if(isset($_POST["update"])){
            $st = $pdo->prepare("UPDATE login SET name=?, password=? WHERE id=?");

            $password = password_hash($_POST["password"], PASSWORD_DEFAULT, array('cost' => 10));
            $st->execute(array(strip_tags($_POST["userID"]), $password, strip_tags($_POST["ID"])));
        } elseif(isset($_POST["delete"])){
            $st = $pdo->prepare("DELETE FROM login WHERE id=? AND name=?");

            $st->execute(array(strip_tags($_POST["ID"]), strip_tags($_POST["userIDhidden"])));
        }
        
        header("location: userregist.html");
    }catch(Exception $e) {
        print("エラー：" . $e->getMessage());
    }