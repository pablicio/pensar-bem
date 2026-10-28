final class LeitorComPendencia extends ExcecaoDeDominio
{
    public function __construct(
        public readonly int $leitorId,
        public readonly Dinheiro $multa,
    ) {
        parent::__construct(sprintf(
            'Há uma multa de %s em aberto.',
            $multa->formatado(),
        ));
    }

    public function tipo(): string
    {
        return 'leitor-com-pendencia';
    }
}
