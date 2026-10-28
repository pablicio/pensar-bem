test('devolução adiantada não gera dias de atraso', function () {
    $prazo = new PrazoDeEmprestimo(
        retirada: new DateTimeImmutable('2026-02-02 10:00'),
        dias: 14,
    );

    $dias = $prazo->diasDeAtraso(
        new DateTimeImmutable('2026-02-13 18:00'),
    );

    expect($dias)->toBe(0);
});
