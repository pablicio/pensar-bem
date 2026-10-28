<?php

require 'conexao.php';

$termo = $_GET['q'] ?? '';

$sql = 'SELECT id, titulo FROM livros WHERE titulo LIKE ?';

$consulta = $pdo->prepare($sql);
$consulta->execute(['%' . $termo . '%']);

foreach ($consulta as $livro) {
    echo $livro['titulo'], "\n";
}
