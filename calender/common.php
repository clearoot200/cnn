<?php
function h($s){
    return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}

function DBConnection(){
    return new PDO("mysql:dbname=", "", "");
}

function loginCheck(){
    // ログイン中でなければログイン画面へ
    if(!isset($_SESSION["name"])){
        header("location: login.html");
        exit;
    }
}

function formatDateTime($month, $day, $year){
    return date("Y-m-d", mktime(0,0,0,strip_tags($month),strip_tags($day),strip_tags($year)));    
}

function getDayOfTheWeek($month, $day, $year){
    return date("w", mktime(0,0,0,strip_tags($month),strip_tags($day),strip_tags($year)));
}

function getLastDay($month, $year){
    return date("t",mktime(0,0,0,strip_tags($month), 1, strip_tags($year)));
}