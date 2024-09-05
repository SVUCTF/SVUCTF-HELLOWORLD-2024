<?php

highlight_file(__FILE__);

$rce = $_GET['rce'];
if (isset($rce)) {
    eval($rce);
}
