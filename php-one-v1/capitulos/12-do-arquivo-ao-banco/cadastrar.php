<?php

$arquivo = 'acervo.json';

$acervo = file_exists($arquivo)
    ? json_decode(file_get_contents($arquivo), true)
    : [];

$acervo[] = [
    'tombo' => (int) $argv[1],
    'titulo' => $argv[2],
];

file_put_contents(
    $arquivo,
    json_encode($acervo, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)
);

echo "acervo com ", count($acervo), " exemplares\n";
