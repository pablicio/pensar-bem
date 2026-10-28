test('devolução adiantada pela caixa não gera multa', function () {
    // o caso da Dona Marlene, em fevereiro
    $regras = new RegrasDeCirculacao();
    $prazo = new PrazoDeEmprestimo(
        new DateTimeImmutable('2026-02-02 10:00'),
        14,
    );

    $multa = $regras->multaPor(
        $prazo,
        new DateTimeImmutable('2026-02-13 18:00'),
    );

    expect($multa)->toEqual(Dinheiro::zero());
});
