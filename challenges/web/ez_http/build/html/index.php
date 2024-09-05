<?php

if (strpos($_SERVER['HTTP_X_FORWARDED_FOR'], "127") === 0) {
    if ($_SERVER["HTTP_REFERER"] === "genshin.edu.cn") {
        if ($_SERVER["HTTP_USER_AGENT"] === "svuctf") {
            echo "flag在小饼干里!";
            setcookie("flag", file_get_contents("/flag"));
        } else {
            echo "请使用 svuctf 浏览器!";
        }
    } else {
        echo "不是 genshin.edu.cn 来的我不要";
    }
} else {
    echo "必须从本地访问!";
}
