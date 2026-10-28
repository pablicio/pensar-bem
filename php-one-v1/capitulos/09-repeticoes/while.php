<?php

$tentativas = 0;
$conectado = false;

while ($tentativas < 3 && !$conectado) {
    $tentativas++;
    echo "Tentativa ", $tentativas, "\n";
    $conectado = ($tentativas === 3);
}
