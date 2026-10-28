final class EsquecerMaisEmprestados
{
    public function __construct(
        private readonly MaisEmprestados $ranking,
    ) {}

    public function handle(EmprestimoRealizado $evento): void
    {
        $this->ranking->esquecer(
            CarbonImmutable::parse(
                $evento->emprestimo->retirado_em,
            ),
        );
    }
}
