<?php

const MULTA_POR_DIA_EM_CENTAVOS = 80;
const TETO_DE_MULTA_EM_CENTAVOS = 2000;

$dias = 12;
$total_em_centavos = $dias * MULTA_POR_DIA_EM_CENTAVOS;

if ($total_em_centavos > TETO_DE_MULTA_EM_CENTAVOS) {
    $total_em_centavos = TETO_DE_MULTA_EM_CENTAVOS;
}

$reais = number_format($total_em_centavos / 100, 2, ',', '.');
echo 'R$ ', $reais, "\n";
