public record Protocolo
{
    public Protocolo(int ano, int sequencial)
    {
        if (ano < 2027)
        {
            throw new ArgumentOutOfRangeException(
                nameof(ano), "A numeração NE começa em 2027.");
        }
        if (sequencial is < 1 or > 999_999)
        {
            throw new ArgumentOutOfRangeException(
                nameof(sequencial), "Sequencial vai de 1 a 999999.");
        }
        Ano = ano;
        Sequencial = sequencial;
    }

    public int Ano { get; }
    public int Sequencial { get; }

    public override string ToString() => $"NE-{Ano}-{Sequencial:D6}";
    public Protocolo Proximo() => new(Ano, Sequencial + 1);
}
