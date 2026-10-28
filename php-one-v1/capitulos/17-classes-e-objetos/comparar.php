<?php

require 'Livro.php';

$a = new Livro('Dom Casmurro', 1899);
$b = new Livro('Dom Casmurro', 1899);
$c = $a;

var_dump($a == $b);
var_dump($a === $b);
var_dump($a === $c);
