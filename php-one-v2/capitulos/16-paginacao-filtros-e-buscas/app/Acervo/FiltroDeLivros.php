final readonly class FiltroDeLivros
{
    public const ORDENS = [
        'titulo', '-titulo', 'ano', '-ano', 'recentes',
    ];

    public function __construct(
        public ?string $busca,
        public ?string $assunto,
        public ?bool $disponivel,
        public ?int $anoMin,
        public string $ordem,
        public int $porPagina,
    ) {}
}
