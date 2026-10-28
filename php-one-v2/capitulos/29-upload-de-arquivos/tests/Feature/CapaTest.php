test('aceita a capa e deixa o trabalho para a fila', function () {
    Storage::fake('local');
    Queue::fake();
    $livro = Livro::factory()->create();

    $this->actingAs(Usuario::factory()->atendente()->create())
        ->postJson("/api/livros/{$livro->id}/capa", [
            'capa' => UploadedFile::fake()
                ->image('capa.jpg', 800, 1200),
        ])
        ->assertStatus(202);

    Queue::assertPushed(PrepararCapa::class);
    expect(Storage::disk('local')->allFiles('capas/originais'))
        ->toHaveCount(1);
});

test('prepara a capa em webp com 600 de largura', function () {
    Storage::fake('local');
    Storage::fake('public');
    $livro = Livro::factory()->create();
    $original = UploadedFile::fake()->image('capa.jpg', 800, 1200)
        ->store('capas/originais', 'local');

    (new PrepararCapa($livro->id, $original))->handle();

    $capa = Storage::disk('public')->get($livro->fresh()->capa);
    [$largura, $altura] = getimagesizefromstring($capa);

    expect([$largura, $altura])->toBe([600, 900]);
    Storage::disk('local')->assertMissing($original);
});
