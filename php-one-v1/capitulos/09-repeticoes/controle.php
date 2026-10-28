<?php

$exemplares = [
    ['tombo' => 812, 'status' => 'restauro'],
    ['tombo' => 907, 'status' => 'disponivel'],
    ['tombo' => 344, 'status' => 'disponivel'],
];

$escolhido = null;

foreach ($exemplares as $exemplar) {
    if ($exemplar['status'] !== 'disponivel') {
        continue;
    }

    $escolhido = $exemplar['tombo'];
    break;
}

echo $escolhido ?? 'nenhum livre', "\n";
