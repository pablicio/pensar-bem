<?php

function somarMultas(array $multas): int
{
    $total = 0;

    foreach ($multas as $valor) {
        $total = $total + $valor;
    }

    return $total;
}

echo somarMultas([50, 240, 2000]), "\n";
