namespace Prefeitura.Dominio;

public record Endereco(string Logradouro, string Numero, string Bairro);

public record Atendimento(DateTime Quando, Servidor Quem, string Descricao)
{
    // para o EF Core
    private Atendimento() : this(default, null!, null!) { }
}

public enum StatusSolicitacao
{
    Aberta,
    EmAnalise,
    EmAtendimento,
    Resolvida,
    Cancelada
}

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

public class Servidor
{
    public Servidor(string matricula, Cidadao pessoa, Secretaria lotacao)
    {
        Matricula = matricula;
        Pessoa = pessoa;
        Lotacao = lotacao;
    }

    // para o EF Core, que preenche as propriedades depois
    private Servidor() : this(null!, null!, null!) { }

    public string Matricula { get; }
    public Cidadao Pessoa { get; }
    public Secretaria Lotacao { get; set; }
    public bool Ativo { get; private set; } = true;

    public void Aposentar() => Ativo = false;
}

public class SolicitacaoEncerradaException : InvalidOperationException
{
    public SolicitacaoEncerradaException(
        int id, StatusSolicitacao status)
        : base($"Solicitação {id} está {status}: sem mudanças.")
    {
        Id = id;
        Status = status;
    }

    public int Id { get; }
    public StatusSolicitacao Status { get; }
}

public class SemProtocoloException : InvalidOperationException
{
    public SemProtocoloException(int id)
        : base($"Solicitação {id} ainda não tem protocolo.")
    {
        Id = id;
    }

    public int Id { get; }
}

public interface INotificador
{
    void Enviar(Cidadao destinatario, string mensagem);
}

public class NotificadorConsole : INotificador
{
    public void Enviar(Cidadao destinatario, string mensagem)
    {
        Console.WriteLine(
            $"[aviso para {destinatario.Nome}] {mensagem}");
    }
}
