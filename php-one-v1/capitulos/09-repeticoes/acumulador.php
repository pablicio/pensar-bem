<?php

$atrasados = [
    ['titulo' => 'O Cortiço', 'dias' => 9],
    ['titulo' => 'Vidas Secas', 'dias' => 2],
    ['titulo' => 'Grande Sertão', 'dias' => 41],
];

$total_de_dias = 0;
$criticos = 0;

foreach ($atrasados as $emprestimo) {
    $total_de_dias = $total_de_dias + $emprestimo['dias'];

    if ($emprestimo['dias'] > 30) {
        $criticos++;
    }
}

echo $total_de_dias, " dias no total\n";
echo $criticos, " caso(s) critico(s)\n";
