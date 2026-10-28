<?php

$atrasados = [
    ['titulo' => 'O Cortiço', 'dias' => 9],
    ['titulo' => 'Vidas', 'dias' => 2],
    ['titulo' => 'Sertão', 'dias' => 41],
];

$criticos = array_filter(
    $atrasados,
    fn(array $e): bool => $e['dias'] > 30
);

$multas = array_map(
    fn(array $e): int => multaEmCentavos($e['dias']),
    $atrasados
);

print_r(array_column($criticos, 'titulo'));
print_r($multas);
