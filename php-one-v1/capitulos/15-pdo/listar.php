<?php

require 'conexao.php';

$sql = 'SELECT id, titulo, ano FROM livros ORDER BY titulo';

foreach ($pdo->query($sql) as $livro) {
    echo $livro['id'], ' - ', $livro['titulo'], "\n";
}
