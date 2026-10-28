<?php

function aplicarEm(array $itens, callable $operacao): array
{
    $saida = [];

    foreach ($itens as $item) {
        $saida[] = $operacao($item);
    }

    return $saida;
}

$centavos = [50, 240, 2000];

print_r(aplicarEm($centavos, fn(int $c): float => $c / 100));
