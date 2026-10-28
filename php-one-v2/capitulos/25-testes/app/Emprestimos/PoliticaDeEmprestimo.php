final class PoliticaDeEmprestimo
{
    public function __construct(
        private readonly RegrasDeCirculacao $regras,
    ) {}

    public function exigirPermitido(
        SituacaoDoPedido $s,
        DateTimeImmutable $quando,
        ?Autorizacao $autorizacao,
    ): void {
        // as mesmas guardas do capítulo de services,
        // lendo de $s em vez de consultar o banco
    }
}
