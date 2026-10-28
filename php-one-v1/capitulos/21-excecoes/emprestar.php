$limite = (int) date('n') === 1 ? 5 : 3;

$abertos = (int) $pdo->query(
    'SELECT COUNT(*) FROM emprestimos
     WHERE leitor_id = ' . $leitorId . ' AND devolvido_em IS NULL'
)->fetchColumn();

if ($abertos >= $limite) {
    throw new LimiteDeEmprestimosAtingido(
        $leitorId,
        $limite,
        $abertos,
    );
}
