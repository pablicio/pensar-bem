<?php

declare(strict_types=1);

$saoPaulo = new DateTimeZone('America/Sao_Paulo');

$devolucao = new DateTimeImmutable('2026-03-10 23:00:00', $saoPaulo);

$emUtc = $devolucao->setTimezone(new DateTimeZone('UTC'));

echo 'local: ', $devolucao->format('Y-m-d H:i T'), "\n";
echo 'utc:   ', $emUtc->format('Y-m-d H:i T'), "\n";
