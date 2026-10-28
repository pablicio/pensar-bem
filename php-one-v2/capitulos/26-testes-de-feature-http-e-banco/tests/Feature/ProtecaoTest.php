test('rotas do leitor exigem autenticação', function (
    string $metodo,
    string $rota,
) {
    $this->json($metodo, $rota)->assertUnauthorized();
})->with([
    ['GET', '/api/eu'],
    ['GET', '/api/emprestimos'],
    ['POST', '/api/emprestimos/1/renovacao'],
    ['POST', '/api/reservas'],
]);
