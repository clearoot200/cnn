<?php
    session_start();

    require_once("common.php");
    if(!(isset($_POST["year"])&&isset($_POST["month"])&&isset($_POST["day"])&&isset($_POST["place"])&&isset($_POST["event"])&&isset($_POST["subject"]))){
        header("location: schedule.html");

        exit;
    }        

    if(!checkdate($_POST["month"], $_POST["day"], $_POST["year"])){
        $_SESSION["errorMessage"] = "日付が不正です。";
        header("location: schedule.html");

        exit;
    }

    if((($_POST["place"]) === "")||(($_POST["event"]) === "")||(($_POST["subject"]) === "")){
        $_SESSION["errorMessage"] = "入力に不備があります";
        header("location: schedule.html");

        exit;
    }

    try{
        $pdo = DBConnection();
        $st = $pdo->prepare("INSERT INTO schedule VALUES(?,?,?,?,?)");

        $plan = formatDateTime($_POST["month"], $_POST["day"], $_POST["year"]);
        $place = strip_tags($_POST["place"]);
        $event = strip_tags($_POST["event"]);
        $subject = strip_tags($_POST["subject"]);
        $remark = strip_tags($_POST["remark"]);

        $st->execute(array($plan, $place, $event, $subject, $remark));

        unset($_SESSION["errorMessage"]);
        header("location: calender.html");
    }catch(Exception $e) {
        print("エラー：" . $e->getMessage());
    }
    