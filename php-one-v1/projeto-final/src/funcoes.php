<?php

declare(strict_types=1);

namespace CasaAmarela;

function carregarEnv(string $caminho): void
{
    if (!is_file($caminho)) {
        return;
    }
    $valores = parse_ini_file($caminho, false, INI_SCANNER_RAW);
    foreach ($valores as $chave => $valor) {
        $_ENV[$chave] ??= $valor;
    }
}

function env(string $chave, ?string $padrao = null): ?string
{
    return $_ENV[$chave] ?? $padrao;
}
