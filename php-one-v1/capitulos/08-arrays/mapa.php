<?php

$exemplar = [
    'tombo' => 812,
    'titulo' => 'O Cortiço',
    'status' => 'disponivel',
];

echo $exemplar['titulo'], "\n";

$exemplar['status'] = 'emprestado';

echo $exemplar['status'], "\n";
