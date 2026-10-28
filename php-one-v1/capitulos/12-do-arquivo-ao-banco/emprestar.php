<?php

$arquivo = 'emprestimos.json';

$emprestimos = file_exists($arquivo)
    ? json_decode(file_get_contents($arquivo), true)
    : [];

echo "li o arquivo: ", count($emprestimos), " emprestimos\n";

sleep(5);

$emprestimos[] = [
    'exemplar' => (int) $argv[1],
    'leitor' => $argv[2],
];

file_put_contents($arquivo, json_encode($emprestimos));

echo "gravei: ", count($emprestimos), " emprestimos\n";
