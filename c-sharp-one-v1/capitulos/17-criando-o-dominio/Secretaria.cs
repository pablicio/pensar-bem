public class Secretaria
{
    public Secretaria(string sigla, string nome)
    {
        Sigla = sigla;
        Nome = nome;
    }

    public string Sigla { get; }
    public string Nome { get; set; }
}
