final class ImportarLote implements ShouldQueue
{
    use Batchable, Queueable;

    public int $timeout = 240;

    public function __construct(public readonly array $linhas) {}

    public function handle(Importador $importador): void
    {
        if ($this->batch()?->cancelled()) {
            return;
        }
        $importador->importar($this->linhas);
    }
}
