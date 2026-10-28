<?php

declare(strict_types=1);

namespace CasaAmarela\Relatorios;

function estaAtrasado(array $e): bool
{
    return $e['dias'] > 14;
}

$emprestimos = [
    ['leitor' => 'Marlene', 'dias' => 20],
    ['leitor' => 'Iolanda', 'dias' => 3],
];

$atrasados = array_filter($emprestimos, estaAtrasado(...));
echo count($atrasados), "\n";

var_dump(estaAtrasado(...) instanceof \Closure);
