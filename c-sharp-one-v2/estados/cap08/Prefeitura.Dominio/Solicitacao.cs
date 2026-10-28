using static Prefeitura.Dominio.StatusSolicitacao;

namespace Prefeitura.Dominio;

public class Solicitacao
{
    private readonly List<Atendimento> _atendimentos = [];

    public Solicitacao(int id, Cidadao solicitante, string assunto,
                       Secretaria secretaria)
    {
        Id = id;
        Solicitante = solicitante;
        Assunto = assunto;
        SecretariaAtual = secretaria;
        Situacao = Aberta;
    }

    // para o EF Core, que preenche as propriedades depois
    private Solicitacao() : this(0, null!, null!, null!) { }

    public int Id { get; }
    public Cidadao Solicitante { get; }
    public string Assunto { get; }
    public StatusSolicitacao Situacao { get; private set; }
    public Protocolo? Protocolo { get; private set; }
    public Secretaria SecretariaAtual { get; private set; }

    public IReadOnlyList<Atendimento> Atendimentos => _atendimentos;

    public void Protocolar(Protocolo protocolo)
    {
        if (Protocolo is not null)
        {
            throw new InvalidOperationException(
                $"Solicitação {Id} já tem o protocolo {Protocolo}.");
        }
        Protocolo = protocolo;
    }

    public void IniciarAnalise() => MudarPara(EmAnalise);

    public void IniciarAtendimento()
    {
        if (Protocolo is null)
        {
            throw new SemProtocoloException(Id);
        }
        MudarPara(EmAtendimento);
    }

    public void Resolver() => MudarPara(Resolvida);
    public void Cancelar() => MudarPara(Cancelada);

    public void Encaminhar(
        Secretaria destino, Servidor quem, string motivo)
    {
        ExigirAberta();
        var descricao = $"Encaminhada de {SecretariaAtual.Sigla} " +
                        $"para {destino.Sigla}: {motivo}";
        _atendimentos.Add(new Atendimento(DateTime.Now, quem, descricao));
        SecretariaAtual = destino;
    }

    public void Registrar(Servidor quem, string descricao)
    {
        ExigirAberta();
        _atendimentos.Add(new Atendimento(DateTime.Now, quem, descricao));
    }

    private void ExigirAberta()
    {
        if (Situacao is Resolvida or Cancelada)
        {
            throw new SolicitacaoEncerradaException(Id, Situacao);
        }
    }

    private void MudarPara(StatusSolicitacao nova)
    {
        ExigirAberta();
        if (!Regras.Permitida(Situacao, nova))
        {
            throw new InvalidOperationException(
                $"Solicitação {Id}: {Situacao} → {nova} não permitido.");
        }
        Situacao = nova;
    }
}
