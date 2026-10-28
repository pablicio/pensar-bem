<?php

require 'conexao.php';

$sql = 'SELECT titulo, ano FROM livros
        WHERE assunto = :assunto
          AND ano >= :desde
        ORDER BY ano';

$consulta = $pdo->prepare($sql);
$consulta->execute([
    'assunto' => 'literatura',
    'desde' => 1900,
]);

foreach ($consulta as $livro) {
    echo $livro['ano'], ' ', $livro['titulo'], "\n";
}
