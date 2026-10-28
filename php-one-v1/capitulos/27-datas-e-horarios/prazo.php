<?php

declare(strict_types=1);

const DOMINGO = 7;

function proximoDiaAberto(
    DateTimeImmutable $dia,
    array $feriados,
): DateTimeImmutable {
    while (
        (int) $dia->format('N') === DOMINGO
        || in_array($dia->format('Y-m-d'), $feriados, true)
    ) {
        $dia = $dia->modify('+1 day');
    }
    return $dia;
}

$feriados = ['2026-04-03', '2026-04-21'];
$fuso = new DateTimeZone('America/Sao_Paulo');

foreach (['2026-03-22', '2026-04-03', '2026-04-21'] as $data) {
    $prazo = new DateTimeImmutable($data, $fuso);
    $aberto = proximoDiaAberto($prazo, $feriados);
    echo $prazo->format('D d/m'), ' -> ';
    echo $aberto->format('D d/m'), "\n";
}
