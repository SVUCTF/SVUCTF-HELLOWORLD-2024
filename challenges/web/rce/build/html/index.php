<?php

highlight_file(__FILE__);

$rce = $_GET['rce'];
eval($rce);
