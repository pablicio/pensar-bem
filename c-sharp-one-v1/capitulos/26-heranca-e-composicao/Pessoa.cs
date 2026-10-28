public class Pessoa
{
    public Pessoa(string nome, string? cpf)
    {
        Nome = nome;
        Cpf = cpf;
    }

    public string Nome { get; protected set; }
    public string? Cpf { get; }
    public string? Email { get; set; }

    public virtual string Descricao() => Nome;
}
