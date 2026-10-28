<?php

$emprestimos = [];
for ($i = 0; $i < 8412; $i++) {
    $emprestimos[] = ['leitor_id' => $i % 1204];
}

$leitores = [];
for ($i = 0; $i < 1204; $i++) {
    $leitores[] = ['id' => $i, 'nome' => "Leitor {$i}"];
}

$inicio = microtime(true);
$linhas = 0;

foreach ($emprestimos as $emprestimo) {
    foreach ($leitores as $leitor) {
        if ($leitor['id'] === $emprestimo['leitor_id']) {
            $linhas++;
            break;
        }
    }
}

printf("%d linhas em %.3f s\n", $linhas, microtime(true) - $inicio);
