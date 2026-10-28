<?php

function linhaDoRecibo(string $titulo, int $centavos): string
{
    if (mb_strlen($titulo) > 30) {
        $titulo = mb_substr($titulo, 0, 29) . '…';
    }

    $valor = number_format($centavos / 100, 2, ',', '.');

    return sprintf('%-30s %9s', $titulo, $valor);
}
