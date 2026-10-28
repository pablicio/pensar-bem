final class ExemplarIndisponivel extends ExcecaoDeDominio
{
    public function __construct(
        public readonly int $tombo,
        public readonly StatusExemplar $estado,
    ) {
        parent::__construct(sprintf(
            'O exemplar %d está %s.',
            $tombo,
            mb_strtolower($estado->rotulo()),
        ));
    }

    public function tipo(): string
    {
        return 'exemplar-indisponivel';
    }

    public function campos(): array
    {
        return ['exemplar_id' => ['Exemplar indisponível.']];
    }
}
