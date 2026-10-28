final readonly class Autorizacao
{
    public function __construct(
        public int $usuarioId,
        public string $motivo,
    ) {}
}
