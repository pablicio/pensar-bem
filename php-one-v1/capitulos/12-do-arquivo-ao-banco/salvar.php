<?php

$acervo = [
    ['tombo' => 812, 'titulo' => 'O Cortiço'],
    ['tombo' => 907, 'titulo' => 'Vidas Secas'],
];

$json = json_encode(
    $acervo,
    JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE
);

file_put_contents('acervo.json', $json);

echo "gravado\n";
