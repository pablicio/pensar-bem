test('observação interna nunca sai pela API', function (
    string $rota,
) {
    $leitor = Leitor::factory()->create([
        'observacao_interna' => 'SEGREDO-DE-TESTE',
    ]);
    $admin = Usuario::factory()->admin()->create();

    $corpo = $this->actingAs($admin)
        ->getJson(str_replace('{id}', $leitor->id, $rota))
        ->assertOk()
        ->getContent();

    expect($corpo)->not->toContain('SEGREDO-DE-TESTE');
})->with([
    '/api/leitores/{id}',
    '/api/leitores?busca=',
    '/api/leitores/{id}/emprestimos',
]);
