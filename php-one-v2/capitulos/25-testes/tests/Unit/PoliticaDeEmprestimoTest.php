test('permite no limite exato de cada regra', function (
    array $muda,
    string $quando,
) {
    $politica = new PoliticaDeEmprestimo(new RegrasDeCirculacao());

    $politica->exigirPermitido(
        situacao($muda),
        new DateTimeImmutable($quando),
        autorizacao: null,
    );

    expect(true)->toBeTrue();
})->with([
    'multa de exatamente R$ 5,00' => [
        ['multaEmAberto' => Dinheiro::emCentavos(500)],
        '2026-03-10',
    ],
    'dois abertos em março' => [
        ['emprestimosAbertos' => 2], '2026-03-10',
    ],
    'quatro abertos em janeiro' => [
        ['emprestimosAbertos' => 4], '2026-01-15',
    ],
    'chegou há exatamente sete dias' => [
        ['adquiridoEm' => new DateTimeImmutable('2026-03-03')],
        '2026-03-10',
    ],
    'último com autorização' => [
        ['ultimoDisponivel' => true], '2026-03-10',
    ],
]);
