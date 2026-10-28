<?php

declare(strict_types=1);

$linhas = file(__DIR__ . '/doacoes.csv');

echo count($linhas), " linhas\n";
echo round(memory_get_peak_usage() / 1048576, 1), " MB\n";
