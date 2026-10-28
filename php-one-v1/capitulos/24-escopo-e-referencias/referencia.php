<?php

declare(strict_types=1);

function aplicarDesconto(array &$emprestimo): void
{
    $emprestimo['multa'] = intdiv($emprestimo['multa'], 2);
}

$e = ['leitor' => 47, 'multa' => 720];
aplicarDesconto($e);

echo $e['multa'], "\n";
