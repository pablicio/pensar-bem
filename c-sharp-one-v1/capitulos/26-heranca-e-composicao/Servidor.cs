public class Servidor
{
    public Servidor(
        string matricula, Cidadao pessoa, Secretaria lotacao)
    {
        Matricula = matricula;
        Pessoa = pessoa;
        Lotacao = lotacao;
    }

    public string Matricula { get; }
    public Cidadao Pessoa { get; }
    public Secretaria Lotacao { get; set; }
    public bool Ativo { get; private set; } = true;

    public void Aposentar() => Ativo = false;
}
