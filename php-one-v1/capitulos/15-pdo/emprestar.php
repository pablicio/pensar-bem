<?php

require 'conexao.php';

$pdo->beginTransaction();

try {
    $c = $pdo->prepare(
        'INSERT INTO emprestimos
           (exemplar_id, leitor_id, retirado_em, devolver_ate)
         VALUES (?, ?, NOW(), ?)'
    );
    $c->execute([1, 1, '2027-02-18']);

    $c = $pdo->prepare(
        'UPDATE exemplares SET estado = ? WHERE id = ?'
    );
    $c->execute(['emprestado', 1]);

    $pdo->commit();
    echo "emprestimo registrado\n";
} catch (PDOException $e) {
    $pdo->rollBack();
    throw $e;
}
