<?php

declare(strict_types=1);

function gravarCsv(string $caminho, array $linhas): void
{
    $temporario = $caminho . '.tmp';
    $arquivo = fopen($temporario, 'w');
    if ($arquivo === false) {
        throw new RuntimeException("não gravou: {$temporario}");
    }

    try {
        fwrite($arquivo, "\xEF\xBB\xBF");
        foreach ($linhas as $linha) {
            fputcsv($arquivo, $linha, separator: ';', escape: '');
        }
    } finally {
        fclose($arquivo);
    }

    rename($temporario, $caminho);
}

gravarCsv(__DIR__ . '/escolhidos.csv', [
    ['titulo', 'autor'],
    ['Vidas Secas', 'Graciliano Ramos'],
    ['O Cortiço', 'Aluísio Azevedo'],
]);
