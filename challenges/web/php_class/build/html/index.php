<?php

include("flag.php");

highlight_file(__FILE__);

class SVUCTF
{
    public $username = "admin";
    public $password = "H3ll0_W0rld!";
    public $vip = false;

    public function login($u, $p)
    {
        if ($this->username === $u && $this->password === $p) {
            $this->vip = true;
        }
        return $this->vip;
    }
}

if (isset($_GET["username"]) && isset($_GET["password"])) {
    $svu = new SVUCTF();
    if ($svu->login($_GET["username"], $_GET["password"])) {
        echo ("Welcome, " . $svu->username . ".<br>");
        echo ("Flag: " . $flag);
    } else {
        echo ("You are not VIP!");
    }
} else {
    echo ("Input your params!");
}
