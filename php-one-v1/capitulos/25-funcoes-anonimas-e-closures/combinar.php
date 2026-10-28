<?php

declare(strict_types=1);

function todos(\Closure ...$regras): \Closure
{
    return function (array $e) use ($regras): bool {
        foreach ($regras as $regra) {
            if (!$regra($e)) {
                return false;
            }
        }
        return true;
    };
}

$paraCobrar = todos(
    fn(array $e): bool => $e['dias'] > 14,
    fn(array $e): bool => !$e['isento'],
    fn(array $e): bool => $e['colecao'] !== 'referencia',
);

$emprestimos = [
    ['dias' => 20, 'isento' => false, 'colecao' => 'geral'],
    ['dias' => 20, 'isento' => true, 'colecao' => 'geral'],
    ['dias' => 3, 'isento' => false, 'colecao' => 'geral'],
];

echo count(array_filter($emprestimos, $paraCobrar)), "\n";
