using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Prefeitura.Dominio;
using Testcontainers.PostgreSql;

namespace Prefeitura.Api.Testes;

public class ApiDaPrefeitura : WebApplicationFactory<Program>, IAsyncLifetime
{
    public const string ChaveDoAplicativo =
        "tlAwkrhueSmMHlaaC16Uv6dGcBo4yurUdIRwkIAtKNA=";

    private readonly PostgreSqlContainer _banco =
        new PostgreSqlBuilder("postgres:17").Build();

    public async Task InitializeAsync()
    {
        await _banco.StartAsync();

        using var escopo = Services.CreateScope();
        var db = escopo.ServiceProvider
            .GetRequiredService<PrefeituraDbContext>();
        await db.Database.MigrateAsync();

        var obras = new Secretaria("SEOB", "Obras");
        var maria = new Cidadao(0, "MARIA G SOUZA") { Cpf = "12345678909" };
        var criada = new DateTimeOffset(2026, 11, 27, 3, 0, 0, TimeSpan.Zero);
        db.AddRange(
            Solicitacao.Restaurar("4211/26", maria, "BURACO", obras,
                criada, StatusSolicitacao.Aberta),
            Solicitacao.Restaurar("4212/26", maria, "ILUMINACAO", obras,
                criada, StatusSolicitacao.EmAnalise));
        await db.SaveChangesAsync();
    }

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseSetting(
            "ConnectionStrings:Principal", _banco.GetConnectionString());
        builder.ConfigureTestServices(servicos =>
            servicos.AddSingleton<INotificador, NotificadorQueAnota>());
    }

    public HttpClient ClienteDoAplicativo()
    {
        var cliente = CreateClient();
        cliente.DefaultRequestHeaders.Add("X-Chave-Api", ChaveDoAplicativo);
        return cliente;
    }

    async Task IAsyncLifetime.DisposeAsync() => await _banco.DisposeAsync();
}

public class NotificadorQueAnota : INotificador
{
    public List<(string Nome, string Texto)> Enviados { get; } = [];

    public Task EnviarAsync(Cidadao destinatario, string mensagem,
                            CancellationToken cancelamento)
    {
        Enviados.Add((destinatario.Nome, mensagem));
        return Task.CompletedTask;
    }
}
