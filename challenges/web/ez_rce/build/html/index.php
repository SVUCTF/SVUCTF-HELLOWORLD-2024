<?php

highlight_file(__FILE__);

$rce = $_GET['rce'];
if (preg_match("/flag|\\s/im", $rce)) {
    die("hacker!");
}
eval($rce);
