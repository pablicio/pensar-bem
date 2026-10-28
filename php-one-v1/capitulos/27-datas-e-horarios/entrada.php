<?php

declare(strict_types=1);

function lerDataBr(
    string $texto,
    DateTimeZone $fuso,
): ?DateTimeImmutable {
    $data = DateTimeImmutable::createFromFormat(
        '!d/m/Y',
        $texto,
        $fuso,
    );
    $avisos = DateTimeImmutable::getLastErrors();
    if ($data === false || $avisos !== false) {
        return null;
    }
    return $data;
}

$fuso = new DateTimeZone('America/Sao_Paulo');
$textos = ['24/03/2026', '31/02/2026', '2026-03-24', '24/3/2026'];
foreach ($textos as $t) {
    $d = lerDataBr($t, $fuso);
    $saida = $d?->format('Y-m-d H:i') ?? 'inválida';
    echo str_pad($t, 11), $saida, "\n";
}
