<?php

declare(strict_types=1);

function diasDeAtraso(
    DateTimeImmutable $prazo,
    DateTimeImmutable $devolvidoEm,
): int {
    $dia = $devolvidoEm->setTimezone($prazo->getTimezone())
        ->setTime(0, 0);
    $intervalo = $prazo->diff($dia);

    return $intervalo->invert === 1 ? 0 : $intervalo->days;
}

$fuso = new DateTimeZone('America/Sao_Paulo');
$prazo = new DateTimeImmutable('2026-03-24', $fuso);

foreach (['2026-03-20 15:00', '2026-03-24 17:50',
          '2026-03-27 09:15'] as $quando) {
    $devolvido = new DateTimeImmutable($quando, $fuso);
    echo $quando, ': ', diasDeAtraso($prazo, $devolvido), "\n";
}

$utc = new DateTimeImmutable(
    '2026-03-25 01:30',
    new DateTimeZone('UTC'),
);
echo 'utc 25/03 01:30: ', diasDeAtraso($prazo, $utc), "\n";
