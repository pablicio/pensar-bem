<?php

$multa_por_dia = 80;

$calcular = fn(int $dias): int => $dias * $multa_por_dia;

echo $calcular(3), "\n";
