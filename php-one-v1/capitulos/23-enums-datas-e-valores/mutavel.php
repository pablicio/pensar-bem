<?php

$prazo = new DateTime('2026-03-10');
$aviso = $prazo;

$aviso->modify('+14 days');

echo $prazo->format('Y-m-d'), "\n";
