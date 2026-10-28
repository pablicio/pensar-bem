<?php

$mes = 1;
$suspenso = true;

if ($suspenso) {
    $limite = 0;
} elseif ($mes === 1) {
    $limite = 5;
} else {
    $limite = 3;
}

echo "Limite deste leitor: ", $limite, "\n";
