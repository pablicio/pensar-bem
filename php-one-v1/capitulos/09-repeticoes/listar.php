<?php

$atrasados = [
    ['titulo' => 'O Cortiço', 'dias' => 9],
    ['titulo' => 'Vidas Secas', 'dias' => 2],
    ['titulo' => 'Grande Sertão', 'dias' => 41],
];

foreach ($atrasados as $emprestimo) {
    echo $emprestimo['titulo'], ' - ',
         $emprestimo['dias'], " dias\n";
}
