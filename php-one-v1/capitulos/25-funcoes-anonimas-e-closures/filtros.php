<?php

declare(strict_types=1);

function atrasadoMaisQue(int $dias): \Closure
{
    return fn(array $e): bool => $e['dias'] > $dias;
}

$paraAviso = atrasadoMaisQue(7);
$paraCobranca = atrasadoMaisQue(14);
$paraBloqueio = atrasadoMaisQue(30);

$emprestimos = [['dias' => 9], ['dias' => 20], ['dias' => 41]];

echo count(array_filter($emprestimos, $paraAviso)), "\n";
echo count(array_filter($emprestimos, $paraCobranca)), "\n";
echo count(array_filter($emprestimos, $paraBloqueio)), "\n";
