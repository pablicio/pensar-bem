<?php

// mesmos $emprestimos e $leitores de antes

$inicio = microtime(true);

$leitor_por_id = [];
foreach ($leitores as $leitor) {
    $leitor_por_id[$leitor['id']] = $leitor;
}

$linhas = 0;
foreach ($emprestimos as $emprestimo) {
    $leitor = $leitor_por_id[$emprestimo['leitor_id']] ?? null;

    if ($leitor !== null) {
        $linhas++;
    }
}

printf("%d linhas em %.3f s\n", $linhas, microtime(true) - $inicio);
