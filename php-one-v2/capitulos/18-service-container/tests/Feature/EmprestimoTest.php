test('avisa o leitor ao emprestar', function () {
    $falso = new EnviadorFalso();
    $this->app->instance(EnviadorDeAviso::class, $falso);

    $this->postJson('/api/emprestimos', [
        'exemplar_id' => 2117,
        'leitor_id' => 47,
    ])->assertCreated();

    expect($falso->enviados)->toHaveCount(1)
        ->and($falso->enviados[0]['leitor'])->toBe(47);
});
