<?php

require 'conexao.php';

$c = $pdo->prepare('SELECT id, titulo FROM livros WHERE id = ?');
$c->execute([1]);
$livro = $c->fetch();

print_r($livro);

$c = $pdo->prepare('SELECT id, titulo FROM livros WHERE ano > ?');
$c->execute([1900]);
$livros = $c->fetchAll();

echo count($livros), " livros\n";

$c = $pdo->prepare('SELECT COUNT(*) FROM livros WHERE assunto = ?');
$c->execute(['literatura']);
$total = $c->fetchColumn();

echo $total, "\n";
