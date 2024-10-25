<?php

highlight_file(__FILE__);

class A
{
    public $str;
    public function __invoke()
    {
        echo ($this->str);
        echo ("还差一步，再看看");
    }
}

class B
{
    public $fun;
    public function __destruct()
    {
        ($this->fun)();
    }
}

class C
{
    public $command;
    public function __toString()
    {
        system($this->command);
        return "好像执行了什么";
    }
}

$data = $_POST['data'];
if (isset($data)) {
    unserialize($data);
} else {
    echo ("你参数呢?");
}
