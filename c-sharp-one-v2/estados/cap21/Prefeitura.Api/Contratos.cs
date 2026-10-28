using System.ComponentModel.DataAnnotations;
using Prefeitura.Dominio;

namespace Prefeitura.Api;

// O que entra
public record NovaSolicitacao(
    [Range(1, int.MaxValue, ErrorMessage = "Informe o cidadão.")]
    int CidadaoId,
    [Required(ErrorMessage = "Informe o assunto.")]
    string Assunto,
    [Required(ErrorMessage = "Informe a secretaria.")]
    [StringLength(4, MinimumLength = 4,
        ErrorMessage = "A secretaria é a sigla, com 4 letras.")]
    string Secretaria);

public record NovoCidadao(
    [Required(ErrorMessage = "Informe o nome.")]
    [StringLength(120, MinimumLength = 3,
        ErrorMessage = "O nome tem de 3 a 120 caracteres.")]
    string Nome,
    [Cpf] string? Cpf,
    [EmailAddress(ErrorMessage = "E-mail inválido.")] string? Email,
    [RegularExpression(@"^\d{10,11}$",
        ErrorMessage = "Celular: DDD e número, só dígitos.")]
    string? Celular);

public record Encaminhamento(string Destino, string Motivo);

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

public record ProtocoloEmitido(string Protocolo);

public record CidadaoCriado(int Id);

public record LinhaAberta(
    string Numero, string Assunto, string Cidadao,
    DateTimeOffset CriadaEm);

public record LinhaRelatorio(string Secretaria, int Total, int Abertas);

public record Pagina<T>(int Total, int Numero, List<T> Itens);
