<?php
    require_once("common.php");

    function parameterCheckUpdate(){
        if(isset($_POST["year"])&&isset($_POST["month"])&&isset($_POST["day"])&&isset($_POST["place"])&&isset($_POST["event"])&&isset($_POST["subject"])&&isset($_POST["remark"])
            &&isset($_POST["olddatetime"])&&isset($_POST["oldplace"])&&isset($_POST["oldevent"])&&isset($_POST["oldsubject"])&&isset($_POST["oldremark"])){
            header("location:" .$_SERVER["HTTP_REFERER"]);
        } 
    }

    function parameterCheckDelet(){
        if(!(isset($_POST["olddatetime"])&&isset($_POST["oldplace"])&&isset($_POST["oldevent"])&&isset($_POST["oldsubject"])&&isset($_POST["oldremark"]))){
            header("location:" .$_SERVER["HTTP_REFERER"]);

            print("delete");
        }
    }

    function executeSQLUpdate($pdo){
        $st = $pdo->prepare("UPDATE schedule SET plan=?,place=?,event=?,subject=?,remark=? WHERE plan=? AND place=? AND event=? AND subject=? AND remark=?");
        
        $plan = formatDateTime($_POST["month"], $_POST["day"], $_POST["year"]);
        $place = strip_tags($_POST["place"]);
        $event = strip_tags($_POST["event"]);
        $subject = strip_tags($_POST["subject"]);
        $remark = strip_tags($_POST["remark"]);

        $st->execute(array($plan, $place, $event, $subject, $remark, $_POST["olddatetime"], $_POST["oldplace"], $_POST["oldevent"], $_POST["oldsubject"], $_POST["oldremark"]));
    }

    function executeSQLDelete($pdo){
        $st = $pdo->prepare("DELETE FROM schedule WHERE plan=? AND place=? AND event=? AND subject=? AND remark=?");
        $plan = strip_tags($_POST["olddatetime"]);
        $place = strip_tags($_POST["oldplace"]);
        $event = strip_tags($_POST["oldevent"]);
        $subject = strip_tags($_POST["oldsubject"]);
        $remark = strip_tags($_POST["oldremark"]);

        $st->execute(array($plan, $place, $event, $subject, $remark));
    }

    if(isset($_POST["update"])){
        parameterCheckUpdate();
    } else if(isset($_POST["delete"])){
        parameterCheckDelet();
    }

    try{
        $pdo = DBConnection();
        
        if(isset($_POST["update"])){
            executeSQLUpdate($pdo);
        } else if(isset($_POST["delete"])){
            executeSQLDelete($pdo);
        }

        header("location: calender.html");
    }catch(Exception $e) {
        print("エラー：" . $e->getMessage());
    }