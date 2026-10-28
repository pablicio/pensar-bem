test('leitor não vê empréstimo de outro leitor', function () {
    $caio = Usuario::factory()->leitor()->create();
    $iolanda = Leitor::factory()->create();
    $alheio = Emprestimo::factory()
        ->for($iolanda)
        ->create();

    $this->actingAs($caio)
        ->getJson("/api/emprestimos/{$alheio->id}")
        ->assertForbidden();
});

test('filtro de leitor não amplia o escopo', function () {
    $caio = Usuario::factory()->leitor()->create();
    Emprestimo::factory()->count(3)->create();

    $this->actingAs($caio)
        ->getJson('/api/emprestimos?leitor_id=211')
        ->assertOk()
        ->assertJsonCount(0, 'data');
});
