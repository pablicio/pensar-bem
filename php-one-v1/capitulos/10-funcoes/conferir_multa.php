<?php

function multaEmCentavos(int $dias): int
{
    if ($dias <= 0) {
        return 0;
    }

    return min($dias * 80, 2000);
}

$casos = [
    [-3, 0],
    [0, 0],
    [1, 80],
    [24, 1920],
    [25, 2000],
    [90, 2000],
];

foreach ($casos as [$dias, $esperado]) {
    $obtido = multaEmCentavos($dias);
    $marca = $obtido === $esperado ? 'ok    ' : 'FALHOU';

    echo $marca, ' ', $dias, ' dias -> ', $obtido, "\n";
}
