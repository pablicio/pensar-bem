test('exemplar em exposição até o sétimo dia', function () {
    $exemplar = Exemplar::factory()->make([
        'adquirido_em' => '2026-03-03',
    ]);

    expect($exemplar->emExposicao(
        new DateTimeImmutable('2026-03-09'),
    ))->toBeTrue();

    expect($exemplar->emExposicao(
        new DateTimeImmutable('2026-03-11'),
    ))->toBeFalse();
});
