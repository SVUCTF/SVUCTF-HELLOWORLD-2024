<?php

if (!isset($_GET['svu'])) {
    echo "GET 方式上传参数 svu，值为 a";
    exit;
}

if ($_GET['svu'] !== "a") {
    echo "GET 参数错误!";
    exit;
}

echo "POST 方式上传参数 ctf，值为 b";

if (!isset($_POST["ctf"])) {
    exit;
}

if ($_POST['ctf'] !== "b") {
    echo "POST 参数错误!";
    exit;
}

echo file_get_contents("/flag");
