using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Prefeitura.Dominio;
using Prefeitura.Infraestrutura;

namespace Prefeitura.Api;

public static class Configuracao
{
    public static IServiceCollection AddDominio(
        this IServiceCollection servicos, IConfiguration configuracao)
    {
        var feriados = configuracao
            .GetSection("Calendario:Feriados")
            .Get<List<DateOnly>>() ?? [];
        servicos.AddSingleton(new Calendario(feriados));
        servicos.AddSingleton(TimeProvider.System);
        servicos.AddScoped<Balcao>();
        return servicos;
    }

    public static IServiceCollection AddApi(this IServiceCollection servicos)
    {
        servicos.ConfigureHttpJsonOptions(opcoes =>
            opcoes.SerializerOptions.Converters.Add(
                new JsonStringEnumConverter()));
        servicos.AddOpenApi();
        servicos.AddValidation();
        servicos.AddProblemDetails();
        servicos.AddExceptionHandler<TratadorDeRegras>();
        servicos.AddHealthChecks()
            .AddDbContextCheck<PrefeituraDbContext>();
        return servicos;
    }

    public static IServiceCollection AddSeguranca(
        this IServiceCollection servicos, IConfiguration configuracao)
    {
        servicos.Configure<OpcoesClientes>(configuracao.GetSection("Api"));
        var tokens = configuracao.GetSection("Tokens");
        servicos.Configure<OpcoesTokens>(tokens);
        servicos.AddSingleton<EmissorDeTokens>();

        var opcoesTokens = tokens.Get<OpcoesTokens>()!;
        servicos
            .AddAuthentication(AutenticacaoPorChave.Esquema)
            .AddScheme<AuthenticationSchemeOptions, AutenticacaoPorChave>(
                AutenticacaoPorChave.Esquema, null)
            .AddJwtBearer(jwt =>
            {
                jwt.MapInboundClaims = false;
                jwt.TokenValidationParameters = new()
                {
                    ValidIssuer = opcoesTokens.Emissor,
                    ValidAudience = opcoesTokens.Publico,
                    IssuerSigningKey = opcoesTokens.ChaveDeAssinatura(),
                    NameClaimType = "name",
                    RoleClaimType = "role",
                };
            });

        var bearer = JwtBearerDefaults.AuthenticationScheme;
        string[] todos = [AutenticacaoPorChave.Esquema, bearer];
        servicos.AddAuthorizationBuilder()
            .SetFallbackPolicy(new AuthorizationPolicyBuilder(todos)
                .RequireAuthenticatedUser()
                .Build())
            .AddPolicy("Atendimento", p => p
                .AddAuthenticationSchemes(bearer)
                .RequireRole("Atendente", "Gestor"))
            .AddPolicy("Gestao", p => p
                .AddAuthenticationSchemes(bearer)
                .RequireRole("Gestor"))
            .AddPolicy("Protocolar", p => p
                .AddAuthenticationSchemes(todos)
                .RequireRole("app", "Atendente", "Gestor"));
        return servicos;
    }
}
