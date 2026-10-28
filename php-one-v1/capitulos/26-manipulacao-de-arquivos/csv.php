<?php

declare(strict_types=1);

function lerCsv(string $caminho): Generator
{
    $arquivo = fopen($caminho, 'r');
    if ($arquivo === false) {
        throw new RuntimeException("não abriu: {$caminho}");
    }

    $ler = fn() => fgetcsv($arquivo, separator: ';', escape: '');

    try {
        $cabecalho = $ler();
        while (($campos = $ler()) !== false) {
            yield array_combine($cabecalho, $campos);
        }
    } finally {
        fclose($arquivo);
    }
}

$total = 0;
$restauro = 0;

foreach (lerCsv(__DIR__ . '/doacoes.csv') as $livro) {
    $total++;
    if ($livro['estado'] === 'restauro') {
        $restauro++;
    }
}

echo "{$total} livros, {$restauro} para restauro\n";
echo round(memory_get_peak_usage() / 1048576, 1), " MB\n";
