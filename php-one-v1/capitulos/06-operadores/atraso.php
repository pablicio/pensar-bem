<?php

$diferenca = 14 - 17;
$dias_de_atraso = max(0, $diferenca);
$multa_em_centavos = $dias_de_atraso * 80;

echo $dias_de_atraso, " dias, ", $multa_em_centavos, " centavos\n";
