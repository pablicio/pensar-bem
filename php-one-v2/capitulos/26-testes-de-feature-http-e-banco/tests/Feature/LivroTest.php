test('cria livro e devolve 201 com Location', function () {
    $atendente = Usuario::factory()->atendente()->create();

    $resposta = $this->actingAs($atendente)
        ->postJson('/api/livros', [
            'titulo' => 'Vidas Secas',
            'autor' => 'Graciliano Ramos',
            'assunto' => 'literatura',
            'isbn' => '978-85-01-00032-5',
        ]);

    $resposta->assertCreated()
        ->assertHeader('Location')
        ->assertJsonPath('data.titulo', 'Vidas Secas')
        ->assertJsonPath('data.isbn', '9788501000325');
});
