<?php

highlight_file(__FILE__);

class SVUCTF
{
    public $username;
    public $password;
    private $vip = false;

    public function __construct($username, $password)
    {
        if ($username === "admin" && $password === "HELLOWORLD") {
            $this->vip = true;
        }
        $this->username = $username;
        $this->password = $password;
    }

    public function getFlag()
    {
        if ($this->vip) {
            include 'flag.php';
            echo $flag;
        } else {
            echo "Welcome to the SVUCTF, " . $this->username;
        }
    }
}

if (isset($_GET["svu_u"]) && isset($_GET["svu_p"])) {
    $svuctf = new SVUCTF($_GET["svu_u"], $_GET["svu_p"]);
    $svuctf->getFlag();
}
