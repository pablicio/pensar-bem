<?php

$suspenso = false;
$mes = 1;

$limite = match (true) {
    $suspenso => 0,
    $mes === 1 => 5,
    default => 3,
};

echo "Limite: ", $limite, "\n";
