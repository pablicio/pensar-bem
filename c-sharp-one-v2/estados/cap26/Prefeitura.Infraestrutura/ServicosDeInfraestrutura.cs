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
        var conexao = configuracao.Exigir("ConnectionStrings:Principal");
        servicos.AddDbContext<PrefeituraDbContext>(opcoes =>
            opcoes
                .UseNpgsql(conexao, npgsql => npgsql.EnableRetryOnFailure(
                    maxRetryCount: 3,
                    maxRetryDelay: TimeSpan.FromSeconds(2),
                    errorCodesToAdd: null))
                .UseSnakeCaseNamingConvention());

        servicos.AddScoped<INumerador, NumeradorDoBanco>();

        var correio = configuracao.Exigir("Correio:Endereco");
        servicos.AddHttpClient<NotificadorEmail>(http =>
            http.BaseAddress = new Uri(correio));

        var smsEndereco = configuracao.Exigir("Sms:Endereco");
        var smsChave = configuracao.Exigir("Sms:Chave");
        servicos.AddHttpClient<NotificadorSms>(http =>
        {
            http.BaseAddress = new Uri(smsEndereco);
            http.DefaultRequestHeaders.Authorization =
                new("Bearer", smsChave);
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
