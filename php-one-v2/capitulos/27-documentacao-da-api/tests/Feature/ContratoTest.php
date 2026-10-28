test('respostas seguem o esquema OpenAPI', function (
    string $metodo,
    string $rota,
    array $corpo,
    int $status,
) {
    $resposta = $this->actingAs(Usuario::factory()->admin()->create())
        ->json($metodo, $rota, $corpo)
        ->assertStatus($status);

    expect($resposta)->toMatchOpenApi(
        base_path('docs/openapi.json'),
    );
})->with('rotas-do-contrato');
