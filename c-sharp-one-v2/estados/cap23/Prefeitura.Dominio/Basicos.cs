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

public abstract class RegraDeNegocioException(
    string codigo, string mensagem)
    : InvalidOperationException(mensagem)
{
    public string Codigo { get; } = codigo;
}

public class SolicitacaoEncerradaException(
    int id, StatusSolicitacao status)
    : RegraDeNegocioException("solicitacao-encerrada",
        $"Solicitação {id} está {status}: sem mudanças.");

public class TransicaoInvalidaException(
    int id, StatusSolicitacao de, StatusSolicitacao para)
    : RegraDeNegocioException("transicao-invalida",
        $"Solicitação {id}: {de} → {para} não permitido.");

public class SemProtocoloException(int id)
    : RegraDeNegocioException("protocolo-ausente",
        $"Solicitação {id} ainda não tem protocolo.");

public class ProtocoloRepetidoException(int id, Protocolo existente)
    : RegraDeNegocioException("protocolo-repetido",
        $"Solicitação {id} já tem o protocolo {existente}.")
{
    public Protocolo Existente { get; } = existente;
}

public interface INotificador
{
    Task EnviarAsync(Cidadao destinatario, string mensagem,
                     CancellationToken cancelamento);
}

public class NotificadorConsole : INotificador
{
    public Task EnviarAsync(Cidadao destinatario, string mensagem,
                            CancellationToken cancelamento)
    {
        Console.WriteLine(
            $"[aviso para {destinatario.Nome}] {mensagem}");
        return Task.CompletedTask;
    }
}
