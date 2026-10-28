using System.Diagnostics;
using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.Options;
using Prefeitura.Infraestrutura;

namespace Prefeitura.Api;

/// <summary>Os modos de linha de comando da API.</summary>
public static class Comandos
{
    public static bool Executar(WebApplication app, string[] args)
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
}
