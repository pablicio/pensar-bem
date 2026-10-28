abstract class ExcecaoDeDominio extends RuntimeException
{
    abstract public function tipo(): string;

    public function status(): int
    {
        return 409;
    }

    public function campos(): ?array
    {
        return null;
    }
}
