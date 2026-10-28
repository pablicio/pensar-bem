<?php

require 'conexao.php';

$sql = 'INSERT INTO livros (titulo, autor, assunto, ano)
        VALUES (:titulo, :autor, :assunto, :ano)';

$consulta = $pdo->prepare($sql);
$consulta->execute([
    'titulo' => 'Memórias Póstumas de Brás Cubas',
    'autor' => 'Machado de Assis',
    'assunto' => 'literatura',
    'ano' => 1881,
]);

$id = (int) $pdo->lastInsertId();

echo "livro ", $id, " cadastrado\n";
