<?php

highlight_file(__FILE__);

if (preg_match("/flag|\\s/im", $_GET['rce'])) {
    die("hacker!");
}

eval($_GET['rce']);