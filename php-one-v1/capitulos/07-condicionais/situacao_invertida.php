<?php

$dias_de_atraso = 9;

if ($dias_de_atraso <= 30) {
    $situacao = 'notificado';
} elseif ($dias_de_atraso <= 7) {
    $situacao = 'atrasado';
} elseif ($dias_de_atraso <= 0) {
    $situacao = 'em dia';
} else {
    $situacao = 'suspenso';
}

echo $situacao, "\n";
