public class Cidadao
{
    public Cidadao(int id, string nome)
    {
        Id = id;
        Nome = nome;
    }

    public int Id { get; set; }
    public string Nome { get; set; }
    public string? Cpf { get; set; }
    public string? Bairro { get; set; }
}
