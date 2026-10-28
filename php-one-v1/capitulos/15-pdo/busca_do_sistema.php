<?php

require 'conexao.php';

$termo = $_GET['q'] ?? '';

$sql = "SELECT id, titulo FROM livros
        WHERE titulo LIKE '%{$termo}%'";

foreach ($pdo->query($sql) as $livro) {
    echo $livro['titulo'], "\n";
}
