namespace Prefeitura.Dominio.Testes;

public class PrazosTestes
{
    private static readonly HashSet<DateOnly> Feriados =
    [
        new(2027, 1, 20),   // São Sebastião
        new(2027, 6, 1),    // aniversário da cidade
    ];

    [Theory]
    [InlineData("2027-05-28", 1, "2027-05-31")]  // sexta + 1
    [InlineData("2027-05-28", 2, "2027-06-02")]  // pula 1º/jun
    [InlineData("2027-01-19", 1, "2027-01-21")]  // pula 20/jan
    public void Soma_dias_uteis(
        string inicio, int dias, string esperado)
    {
        var resultado = Prazos.SomarDiasUteis(
            DateOnly.Parse(inicio), dias, Feriados);

        Assert.Equal(DateOnly.Parse(esperado), resultado);
    }
}
