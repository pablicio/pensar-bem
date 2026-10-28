using Prefeitura.Api;
using Prefeitura.Api.Endpoints;
using Prefeitura.Infraestrutura;

var builder = WebApplication.CreateBuilder(args);

builder.Services
    .AddInfraestrutura(builder.Configuration)
    .AddDominio(builder.Configuration)
    .AddSeguranca(builder.Configuration)
    .AddApi();

var app = builder.Build();

if (await Comandos.ExecutarAsync(app, args))
{
    return;
}

app.UseExceptionHandler();
app.UseStatusCodePages();
app.UseAuthentication();
app.UseAuthorization();

app.MapHealthChecks("/saude").AllowAnonymous();
if (!app.Environment.IsProduction())
{
    app.MapOpenApi().AllowAnonymous();
}

app.MapSolicitacoes();
app.MapCadastros();
app.MapRelatorios();

app.Run();

public partial class Program;
