<?php

function linhaDoRecibo(string $titulo, int $centavos): string
{
    $titulo = str_pad(substr($titulo, 0, 30), 30);
    $valor = number_format($centavos / 100, 2, ',', '.');

    return $titulo . str_pad($valor, 10, ' ', STR_PAD_LEFT);
}

echo linhaDoRecibo('Memórias Póstumas de Brás Cubas', 720), "\n";
echo linhaDoRecibo('O Cortiço', 720), "\n";
