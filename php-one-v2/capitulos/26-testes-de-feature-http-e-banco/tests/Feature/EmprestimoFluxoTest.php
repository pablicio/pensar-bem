test('empréstimo grava e trava o exemplar juntos', function () {
    $exemplar = Exemplar::factory()->disponivel()->create();
    $leitor = Leitor::factory()->emDia()->create();
    $atendente = Usuario::factory()->atendente()->create();

    $this->actingAs($atendente)
        ->postJson('/api/emprestimos', [
            'exemplar_id' => $exemplar->id,
            'leitor_id' => $leitor->id,
        ])
        ->assertCreated();

    $this->assertDatabaseHas('emprestimos', [
        'exemplar_id' => $exemplar->id,
        'leitor_id' => $leitor->id,
        'devolvido_em' => null,
    ]);

    expect($exemplar->fresh()->estado)
        ->toBe(StatusExemplar::Emprestado);
});
