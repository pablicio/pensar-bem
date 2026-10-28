<?php

declare(strict_types=1);

function aplicarDesconto(array $emprestimo): array
{
    $emprestimo['multa'] = intdiv($emprestimo['multa'], 2);
    return $emprestimo;
}

$e = ['leitor' => 47, 'multa' => 720];
$comDesconto = aplicarDesconto($e);

echo $e['multa'], "\n";
echo $comDesconto['multa'], "\n";
