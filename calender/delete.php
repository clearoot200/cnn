<?php
    require_once("common.php");
    if(!(isset($_POST["deletedatetime"])&&isset($_POST["deleteplace"])&&isset($_POST["deleteevent"])&&isset($_POST["deletesubject"])&&isset($_POST["deleteremark"]))){
        header("location: confirm.html");
    }

    try{
        $pdo = DBConnection();
        $st = $pdo->prepare("DELETE FROM schedule WHERE plan=? AND place=? AND event=? AND subject=? AND remark=?");
        $plan = strip_tags($_POST["deletedatetime"]);
        $place = strip_tags($_POST["deleteplace"]);
        $event = strip_tags($_POST["deleteevent"]);
        $subject = strip_tags($_POST["deletesubject"]);
        $remark = strip_tags($_POST["deleteremark"]);

        $st->execute(array($plan, $place, $event, $subject, $remark));
        
        header("location: calender.html");
    }catch(Exception $e) {
        print("エラー：" . $e->getMessage());
    }