<?php

require 'conexao.php';

$sql = 'UPDATE emprestimos
        SET devolvido_em = NOW()
        WHERE id = ? AND devolvido_em IS NULL';

$consulta = $pdo->prepare($sql);
$consulta->execute([3315]);

if ($consulta->rowCount() === 0) {
    echo "emprestimo inexistente ou ja devolvido\n";
} else {
    echo "devolucao registrada\n";
}
