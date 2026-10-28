beforeEach(function () {
    $this->dono = Usuario::factory()->leitor()->create();
    $this->outro = Usuario::factory()->leitor()->create();
    $this->atendente = Usuario::factory()->atendente()->create();

    $this->emprestimo = Emprestimo::factory()
        ->for($this->dono->leitor)
        ->create();
});

test('dono vê o próprio empréstimo', function () {
    $this->actingAs($this->dono)
        ->getJson("/api/emprestimos/{$this->emprestimo->id}")
        ->assertOk();
});

test('outro leitor não vê', function () {
    $this->actingAs($this->outro)
        ->getJson("/api/emprestimos/{$this->emprestimo->id}")
        ->assertForbidden();
});

test('atendente vê', function () {
    $this->actingAs($this->atendente)
        ->getJson("/api/emprestimos/{$this->emprestimo->id}")
        ->assertOk();
});
