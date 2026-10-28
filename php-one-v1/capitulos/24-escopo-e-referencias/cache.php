<?php

declare(strict_types=1);

function multaDiaria(): int
{
    static $valor = null;

    if ($valor === null) {
        echo "(lendo config)\n";
        $valor = 80;
    }

    return $valor;
}

echo multaDiaria(), "\n";
echo multaDiaria(), "\n";
