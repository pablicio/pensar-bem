final readonly class SituacaoDoPedido
{
    public function __construct(
        public StatusExemplar $estadoDoExemplar,
        public bool $daReferencia,
        public bool $daColecaoFechada,
        public ?DateTimeImmutable $adquiridoEm,
        public bool $ultimoDisponivel,
        public bool $leitorAtivo,
        public bool $leitorInfantil,
        public int $emprestimosAbertos,
        public int $emprestimosAtrasados,
        public Dinheiro $multaEmAberto,
    ) {}
}
