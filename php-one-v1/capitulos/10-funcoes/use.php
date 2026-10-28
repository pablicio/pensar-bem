<?php

$multa_por_dia = 80;

$calcular = function (int $dias) use ($multa_por_dia): int {
    return $dias * $multa_por_dia;
};

echo $calcular(3), "\n";

$multa_por_dia = 150;
echo $calcular(3), "\n";
