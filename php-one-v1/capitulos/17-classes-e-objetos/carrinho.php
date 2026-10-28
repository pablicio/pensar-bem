<?php

require 'Livro.php';

$original = new Livro('Dom Casmurro', 1899);
$copia = $original;

$copia->ano = 1900;

echo $original->ano, "\n";
var_dump($original == $copia);
