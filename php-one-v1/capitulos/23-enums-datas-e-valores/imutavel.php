<?php

$prazo = new DateTimeImmutable('2026-03-10');
$aviso = $prazo->add(new DateInterval('P14D'));

echo 'prazo: ', $prazo->format('Y-m-d'), "\n";
echo 'aviso: ', $aviso->format('Y-m-d'), "\n";
