using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Prefeitura.Dominio;

namespace Prefeitura.Infraestrutura;

public static class ServicosDeInfraestrutura
{
    public static IServiceCollection AddInfraestrutura(
        this IServiceCollection servicos, IConfiguration configuracao)
    {
        var conexao = configuracao.GetConnectionString("Principal");
        servicos.AddDbContext<PrefeituraDbContext>(opcoes =>
            opcoes
                .UseNpgsql(conexao, npgsql => npgsql.EnableRetryOnFailure(
                    maxRetryCount: 3,
                    maxRetryDelay: TimeSpan.FromSeconds(2),
                    errorCodesToAdd: null))
                .UseSnakeCaseNamingConvention());

        servicos.AddScoped<INumerador, NumeradorDoBanco>();

        var correio = configuracao["Correio:Endereco"]!;
        servicos.AddHttpClient<NotificadorEmail>(http =>
            http.BaseAddress = new Uri(correio));

        var sms = configuracao.GetSection("Sms");
        servicos.AddHttpClient<NotificadorSms>(http =>
        {
            http.BaseAddress = new Uri(sms["Endereco"]!);
            http.DefaultRequestHeaders.Authorization =
                new("Bearer", sms["Chave"]);
        });

        servicos.AddScoped<INotificador>(sp => new NotificadorMultiplo(
            sp.GetRequiredService<ILogger<NotificadorMultiplo>>(),
            sp.GetRequiredService<NotificadorEmail>(),
            sp.GetRequiredService<NotificadorSms>()));

        servicos
            .AddOptions<OpcoesSip>()
            .Bind(configuracao.GetSection("Sip"))
            .ValidateDataAnnotations()
            .ValidateOnStart();

        return servicos;
    }
}
