<?php

$titulo = '  O   Cortiço  ';

$limpo = trim($titulo);
$limpo = preg_replace('/\s+/u', ' ', $limpo);

var_dump($limpo);
var_dump(str_contains($limpo, 'Cort'));
var_dump(str_starts_with($limpo, 'O '));
var_dump(str_ends_with($limpo, 'ço'));
