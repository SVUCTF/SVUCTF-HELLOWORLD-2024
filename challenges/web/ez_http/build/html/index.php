<?php

$forwardedFor = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? null;
$referer = $_SERVER["HTTP_REFERER"] ?? null;
$userAgent = $_SERVER["HTTP_USER_AGENT"] ?? null;

if ($forwardedFor === null || strpos($forwardedFor, "127") !== 0) {
    echo "必须从本地访问!";
    exit;
}

if ($referer !== "genshin.edu.cn") {
    echo "不是 genshin.edu.cn 来的我不要";
    exit;
}

if ($userAgent !== "svuctf") {
    echo "请使用 svuctf 浏览器!";
    exit;
}

setcookie("flag", file_get_contents("/flag"));
echo "flag在小饼干里!";
