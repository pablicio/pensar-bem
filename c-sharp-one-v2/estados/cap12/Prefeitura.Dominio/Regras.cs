using Microsoft.Extensions.Logging;
using static Prefeitura.Dominio.StatusSolicitacao;

namespace Prefeitura.Dominio;

public static class Regras
{
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

public interface INumerador
{
    Protocolo Proximo();
}

public class Numerador : INumerador
{
    private Protocolo? _ultimo;

    public Numerador(Protocolo? ultimoEmitido) =>
        _ultimo = ultimoEmitido;

    public Protocolo Proximo()
    {
        _ultimo = _ultimo?.Proximo() ?? new Protocolo(2027, 1);
        return _ultimo;
    }
}

public class Balcao(
    INumerador numerador, INotificador notificador,
    ILogger<Balcao> logger)
{
    public void Protocolar(Solicitacao s)
    {
        if (s.Protocolo is not null)
        {
            logger.LogWarning(
                "Protocolo repetido para {SolicitacaoId}; já é {Protocolo}",
                s.Id, s.Protocolo);
            throw new InvalidOperationException(
                $"Solicitação {s.Id} já tem o protocolo {s.Protocolo}.");
        }

        logger.LogInformation(
            "Protocolando solicitação {SolicitacaoId}", s.Id);

        var protocolo = numerador.Proximo();
        s.Protocolar(protocolo);

        logger.LogInformation(
            "Solicitação {SolicitacaoId} protocolada: {Protocolo}",
            s.Id, protocolo);

        var aviso = $"Seu protocolo: {protocolo}";
        notificador.Enviar(s.Solicitante, aviso);
    }
}
