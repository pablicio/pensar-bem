using Prefeitura.Dominio;

namespace Prefeitura.Api;

// O que entra
public record NovaSolicitacao(
    int CidadaoId, string Assunto, string Secretaria);

public record Encaminhamento(
    string Destino, string Matricula, string Motivo);

// O que sai
public record SolicitacaoResumo(
    int Id, string Assunto, StatusSolicitacao Situacao,
    string Secretaria, DateTimeOffset CriadaEm);

public record SolicitacaoDetalhe(
    int Id, string? NumeroSip, string? Protocolo, string Assunto,
    StatusSolicitacao Situacao, SecretariaResposta Secretaria,
    DateTimeOffset CriadaEm, List<AtendimentoResposta> Atendimentos);

public record SecretariaResposta(string Sigla, string Nome);

public record AtendimentoResposta(DateTime Quando, string Descricao);

public record LinhaRelatorio(string Secretaria, int Total, int Abertas);

public record Pagina<T>(int Total, int Numero, List<T> Itens);
