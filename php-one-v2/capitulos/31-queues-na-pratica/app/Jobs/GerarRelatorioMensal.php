final class GerarRelatorioMensal implements
    ShouldQueue,
    ShouldBeUnique
{
    use Queueable;

    public int $uniqueFor = 3600;

    public function __construct(public readonly string $mes) {}

    public function uniqueId(): string
    {
        return $this->mes;
    }
}
