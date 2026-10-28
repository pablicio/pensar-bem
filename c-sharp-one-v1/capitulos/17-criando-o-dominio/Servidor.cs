public class Servidor
{
    public Servidor(string matricula, string nome, Secretaria lotacao)
    {
        Matricula = matricula;
        Nome = nome;
        Lotacao = lotacao;
    }

    public string Matricula { get; }
    public string Nome { get; }
    public Secretaria Lotacao { get; set; }
}
