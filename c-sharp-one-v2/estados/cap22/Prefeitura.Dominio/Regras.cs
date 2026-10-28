using Microsoft.Extensions.Logging;
using static Prefeitura.Dominio.StatusSolicitacao;

namespace Prefeitura.Dominio;

public static class Regras
{
    public static readonly IReadOnlySet<string> Assuntos =
        new HashSet<string>
        {
            "BURACO", "ILUMINACAO", "CALCADA", "PODA", "ENTULHO",
            "2A VIA IPTU", "ALVARA", "AGENDAMENTO", "VAGA CRECHE",
            "TRANSFERENCIA ESCOLAR", "PONTO DE ONIBUS", "LINHA DE ONIBUS",
        };

    public static int PrazoEmDias(string assunto) => assunto switch
    {
        "BURACO" => 15,
        "ILUMINACAO" => 10,
        "PODA" => 30,
        "2A VIA IPTU" => 1,
        _ => 30
    };

    public static bool ExigeCpf(string assunto) =>
        assunto is "2A VIA IPTU" or "ALVARA";

    internal static bool Permitida(
        StatusSolicitacao de, StatusSolicitacao para) =>
        (de, para) switch
        {
            (Aberta, EmAnalise) => true,
            (Aberta, EmAtendimento) => true,     // 2ª via, no balcão
            (EmAnalise, EmAtendimento) => true,
            (EmAtendimento, Resolvida) => true,
            (Resolvida, _) => false,
            (Cancelada, _) => false,
            (_, Cancelada) => true,
            _ => false
        };
}

public static class Prazos
{
    public static DateOnly SomarDiasUteis(
        DateOnly inicio, int dias, IReadOnlySet<DateOnly> feriados)
    {
        var data = inicio;
        var contados = 0;

        while (contados < dias)
        {
            data = data.AddDays(1);

            var fimDeSemana = data.DayOfWeek
                is DayOfWeek.Saturday or DayOfWeek.Sunday;
            if (fimDeSemana)
            {
                continue;
            }
            if (feriados.Contains(data))
            {
                continue;
            }
            contados++;
        }
        return data;
    }
}

public class Calendario(IEnumerable<DateOnly> feriados)
{
    private readonly HashSet<DateOnly> _feriados = [.. feriados];

    public DateOnly PrazoFinal(DateOnly inicio, string assunto) =>
        Prazos.SomarDiasUteis(
            inicio, Regras.PrazoEmDias(assunto), _feriados);
}

public interface INumerador
{
    Task<Protocolo> ProximoAsync(CancellationToken cancelamento);
}

public class Numerador : INumerador
{
    private Protocolo? _ultimo;

    public Numerador(Protocolo? ultimoEmitido) =>
        _ultimo = ultimoEmitido;

    public Task<Protocolo> ProximoAsync(CancellationToken cancelamento)
    {
        _ultimo = _ultimo?.Proximo() ?? new Protocolo(2027, 1);
        return Task.FromResult(_ultimo);
    }
}

public class Balcao(
    INumerador numerador, INotificador notificador,
    Calendario calendario, TimeProvider relogio,
    ILogger<Balcao> logger)
{
    private static readonly TimeZoneInfo Brasilia =
        TimeZoneInfo.FindSystemTimeZoneById("America/Sao_Paulo");

    public async Task ProtocolarAsync(
        Solicitacao s, CancellationToken cancelamento)
    {
        if (s.Protocolo is not null)
        {
            logger.LogWarning(
                "Protocolo repetido para {SolicitacaoId}; já é {Protocolo}",
                s.Id, s.Protocolo);
            throw new ProtocoloRepetidoException(s.Id, s.Protocolo);
        }

        logger.LogInformation(
            "Protocolando solicitação {SolicitacaoId}", s.Id);

        var protocolo = await numerador.ProximoAsync(cancelamento);
        var agora = TimeZoneInfo.ConvertTime(
            relogio.GetUtcNow(), Brasilia);
        var hoje = DateOnly.FromDateTime(agora.DateTime);
        var prazo = calendario.PrazoFinal(hoje, s.Assunto);
        s.Protocolar(protocolo, prazo);

        logger.LogInformation(
            "Solicitação {SolicitacaoId}: número reservado {Protocolo}",
            s.Id, protocolo);
    }

    public Task AvisarAsync(Solicitacao s, CancellationToken cancelamento)
    {
        var aviso = $"Seu protocolo: {s.Protocolo}. " +
                    $"Prazo: até {s.PrazoEm:dd/MM/yyyy}.";
        return notificador.EnviarAsync(s.Solicitante, aviso, cancelamento);
    }
}
