<?php

declare(strict_types=1);

$arquivo = fopen(__DIR__ . '/doacoes.csv', 'r');
if ($arquivo === false) {
    throw new RuntimeException('doacoes.csv não abriu');
}

$total = 0;
try {
    while (($linha = fgets($arquivo)) !== false) {
        $total++;
    }
} finally {
    fclose($arquivo);
}

echo "{$total} linhas\n";
