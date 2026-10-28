<?php

require 'conexao.php';

function buscarLivros(
    PDO $pdo,
    string $termo,
    int $limite = 20,
): array {
    $sql = 'SELECT l.id, l.titulo, l.autor,
                   COUNT(e.id) AS exemplares
            FROM livros l
            LEFT JOIN exemplares e ON e.livro_id = l.id
            WHERE l.titulo LIKE :termo OR l.autor LIKE :termo
            GROUP BY l.id, l.titulo, l.autor
            ORDER BY l.titulo
            LIMIT :limite';

    $consulta = $pdo->prepare($sql);
    $consulta->bindValue('termo', '%' . $termo . '%');
    $consulta->bindValue('limite', $limite, PDO::PARAM_INT);
    $consulta->execute();

    return $consulta->fetchAll();
}

foreach (buscarLivros($pdo, 'assis') as $livro) {
    printf("%-35s %s (%d)\n",
        $livro['titulo'], $livro['autor'], $livro['exemplares']);
}
