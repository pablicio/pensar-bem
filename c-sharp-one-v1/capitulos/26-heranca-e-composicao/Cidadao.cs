public class Cidadao
{
    public Cidadao(int id, string nome) { Id = id; Nome = nome; }

    public int Id { get; }
    public string Nome { get; set; }
    public string? Cpf { get; set; }
    public string? Email { get; set; }
    public Endereco? Endereco { get; set; }
}
