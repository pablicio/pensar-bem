<?php

require 'vendor/autoload.php';
require 'conexao.php';

$livros = $pdo->query(
    'SELECT id, titulo, ano FROM livros ORDER BY titulo LIMIT 2'
)->fetchAll();

dump($livros);
