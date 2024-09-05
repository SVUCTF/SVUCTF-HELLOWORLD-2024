<?php

$getParam = $_GET['svu'];
$postParam = $_POST['ctf'];

if (isset($getParam) && isset($postParam)) {
    if ($getParam === "a") {
        echo ("POST 方式上传参数 ctf，值为 b");
        if ($postParam === "b") {
            echo file_get_contents("/flag");
        } else {
            echo ("POST 参数错误!");
        }
    } else {
        echo ("GET 参数错误!");
    }
} else {
    echo ("GET 方式上传参数 svu，值为 a");
}
