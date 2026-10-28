<?php

require 'vendor/autoload.php';
require 'conexao.php';

use CasaAmarela\Acervo\Livro;

$linhas = $pdo->query('SELECT titulo, ano FROM livros')->fetchAll();

foreach ($linhas as $linha) {
    $livro = new Livro($linha['titulo'], (int) $linha['ano']);
    echo $livro->titulo, "\n";
}
