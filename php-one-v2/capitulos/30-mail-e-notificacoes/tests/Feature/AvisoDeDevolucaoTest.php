test('avisa por e-mail e WhatsApp quem aceitou os dois', function () {
    Notification::fake();
    $emprestimo = Emprestimo::factory()
        ->venceAmanha()
        ->for(Leitor::factory()->comEmail()->aceitaWhatsApp())
        ->create();

    $this->artisan('schedule:test', [
        '--name' => 'avisos-de-devolucao',
    ]);

    Notification::assertSentTo(
        $emprestimo->leitor,
        DevolucaoAmanha::class,
        fn ($aviso, array $canais) => $canais === [
            'mail', CanalWhatsApp::class, 'database',
        ],
    );
});

test('e-mail em português, assinado pela Casa Amarela', function () {
    config(['app.name' => 'Biblioteca Casa Amarela']);
    app()->setLocale('pt_BR');
    $emprestimo = Emprestimo::factory()->venceAmanha()->create();

    $html = (string) (new DevolucaoAmanha($emprestimo))
        ->toMail($emprestimo->leitor)
        ->render();

    expect($html)
        ->toContain('Biblioteca Casa Amarela')
        ->toContain('Até logo')
        ->not->toContain('Laravel')
        ->not->toContain('Regards');
});
