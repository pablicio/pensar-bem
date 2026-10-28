using System.Diagnostics;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using Prefeitura.Dominio;
using Prefeitura.Infraestrutura;

namespace Prefeitura.Api;

/// <summary>Os modos de linha de comando da API.</summary>
public static class Comandos
{
    public static async Task<bool> ExecutarAsync(
        WebApplication app, string[] args)
    {
        switch (args)
        {
            case ["nova-chave"]:
                NovaChave();
                return true;
            case ["importar"]:
                Importar(app);
                return true;
            case ["credencial", var matricula, var papel]:
                Credencial(app, matricula, papel);
                return true;
            case ["recalcular-prazos", var dia, var matricula]:
                await RecalcularPrazosAsync(
                    app, DateOnly.Parse(dia), matricula);
                return true;
            default:
                return false;
        }
    }

    private static void NovaChave()
    {
        var chave = Chaves.Nova();
        var hash = Convert.ToHexString(Chaves.Hash(chave));
        Console.WriteLine($"chave: {chave}");
        Console.WriteLine($"hash: {hash}");
    }

    private static void Importar(WebApplication app)
    {
        using var escopo = app.Services.CreateScope();
        var servicos = escopo.ServiceProvider;
        var db = servicos.GetRequiredService<PrefeituraDbContext>();
        var sip = servicos
            .GetRequiredService<IOptions<OpcoesSip>>().Value;

        var relogio = Stopwatch.StartNew();
        var secretarias = db.Secretarias.ToDictionary(s => s.Sigla);
        if (secretarias.Count == 0)
        {
            secretarias = ImportacaoSip.SecretariasPadrao()
                .ToDictionary(s => s.Sigla);
        }
        var cidadaos = db.Cidadaos
            .Where(c => c.Cpf != null)
            .ToDictionary(c => c.Cpf!);
        var lidas = ImportacaoSip.Carregar(
            sip.CaminhoCsv, sip.Encoding, secretarias, cidadaos);
        db.AddRange(lidas);
        db.SaveChanges();

        app.Logger.LogInformation(
            "{Quantas} solicitações importadas em {Tempo}",
            lidas.Count, relogio.Elapsed);
    }

    private static void Credencial(
        WebApplication app, string matricula, string papel)
    {
        using var escopo = app.Services.CreateScope();
        var db = escopo.ServiceProvider
            .GetRequiredService<PrefeituraDbContext>();
        Console.Write("Senha: ");
        var senha = Console.ReadLine() ?? "";
        var credencial = new Credencial
        {
            Matricula = matricula,
            Papel = papel
        };
        credencial.HashDaSenha = new PasswordHasher<Credencial>()
            .HashPassword(credencial, senha);
        db.Credenciais.Add(credencial);
        db.SaveChanges();
        Console.WriteLine($"Credencial de {matricula} gravada.");
    }

    private static async Task RecalcularPrazosAsync(
        WebApplication app, DateOnly dia, string matricula)
    {
        using var escopo = app.Services.CreateScope();
        var servicos = escopo.ServiceProvider;
        var db = servicos.GetRequiredService<PrefeituraDbContext>();
        var calendario = servicos.GetRequiredService<Calendario>();
        var balcao = servicos.GetRequiredService<Balcao>();
        var quem = db.Servidores.Find(matricula)
            ?? throw new InvalidOperationException(
                $"Servidor {matricula} não encontrado.");

        // O banco não guarda a hora do protocolo; a da criação serve,
        // porque o aplicativo e o balcão criam e protocolam juntos.
        var fuso = TimeZoneInfo.FindSystemTimeZoneById(
            "America/Sao_Paulo");
        var de = new DateTimeOffset(TimeZoneInfo.ConvertTimeToUtc(
            dia.ToDateTime(TimeOnly.MinValue), fuso));
        var ate = de.AddDays(1);
        var doDia = await db.Solicitacoes
            .Include(s => s.Solicitante)
            .Where(s => s.Protocolo != null
                        && s.CriadaEm >= de && s.CriadaEm < ate
                        && s.Situacao != StatusSolicitacao.Resolvida
                        && s.Situacao != StatusSolicitacao.Cancelada)
            .OrderBy(s => s.Id)
            .ToListAsync();

        const string Motivo =
            "protocolo em dia não útil conta do dia útil seguinte";
        var corrigidas = new List<Solicitacao>();
        foreach (var s in doDia)
        {
            var antes = s.PrazoEm;
            var certo = calendario.PrazoFinal(dia, s.Assunto);
            s.CorrigirPrazo(certo, quem, Motivo);
            if (s.PrazoEm != antes)
            {
                Console.WriteLine(
                    $"{s.Protocolo}  {s.Assunto,-11}  " +
                    $"{antes:dd/MM} -> {s.PrazoEm:dd/MM}");
                corrigidas.Add(s);
            }
        }
        await db.SaveChangesAsync();

        foreach (var s in corrigidas)
        {
            await balcao.AvisarAsync(s, CancellationToken.None);
        }
        Console.WriteLine(
            $"{doDia.Count} protocolos do dia, " +
            $"{corrigidas.Count} prazos corrigidos.");
    }
}
