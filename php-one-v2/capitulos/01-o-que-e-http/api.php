<?php

declare(strict_types=1);

header('Content-Type: application/json');

$emprestimos = [
    4471 => ['exemplar_id' => 812, 'leitor_id' => 47],
];

$caminho = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($_SERVER['REQUEST_METHOD'] === 'GET'
    && preg_match('#^/emprestimos/(\d+)$#', $caminho, $partes)) {

    $id = (int) $partes[1];

    if (!isset($emprestimos[$id])) {
        http_response_code(404);
        echo json_encode(['erro' => "Empréstimo {$id} não existe"]);
        exit;
    }

    echo json_encode(['id' => $id] + $emprestimos[$id]);
    exit;
}

http_response_code(404);
echo json_encode(['erro' => 'Rota não encontrada']);
