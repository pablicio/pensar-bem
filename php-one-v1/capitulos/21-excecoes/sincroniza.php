<?php

$arquivo = fopen('/tmp/editora.csv', 'r');

if ($arquivo === false) {
    throw new RuntimeException('CSV da editora não chegou');
}

$gravadas = 0;
$rejeitadas = [];

try {
    while (($linha = fgetcsv($arquivo)) !== false) {
        try {
            gravar($pdo, $linha);
            $gravadas++;
        } catch (LinhaInvalida $e) {
            $rejeitadas[] = $e->getMessage();
            error_log((string) $e);
        }
    }
} finally {
    fclose($arquivo);
}

echo "gravadas: {$gravadas}, rejeitadas: ", count($rejeitadas), "\n";

exit($rejeitadas === [] ? 0 : 1);
