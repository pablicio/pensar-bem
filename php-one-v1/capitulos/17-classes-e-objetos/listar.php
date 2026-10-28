<?php

require 'conexao.php';
require 'acervo.php';

$sql = 'SELECT e.tombo, e.estado, l.titulo, l.ano
        FROM exemplares e
        JOIN livros l ON l.id = e.livro_id
        ORDER BY l.titulo';

foreach ($pdo->query($sql) as $linha) {
    $exemplar = exemplarDeLinha($linha);
    echo $exemplar->tombo, ' — ', $exemplar->livro, "\n";
}
