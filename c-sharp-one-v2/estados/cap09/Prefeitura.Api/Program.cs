using System.Text.Json.Serialization;
using Microsoft.EntityFrameworkCore;
using Prefeitura.Api;
using Prefeitura.Dominio;

var builder = WebApplication.CreateBuilder(args);

builder.Services.ConfigureHttpJsonOptions(opcoes =>
    opcoes.SerializerOptions.Converters.Add(
        new JsonStringEnumConverter()));

builder.Services
    .AddOptions<OpcoesSip>()
    .Bind(builder.Configuration.GetSection("Sip"))
    .ValidateDataAnnotations()
    .ValidateOnStart();

var caminho = builder.Configuration["Sip:CaminhoCsv"]
    ?? throw new InvalidOperationException(
        "Sip:CaminhoCsv não configurado.");
var dados = ImportacaoSip.Carregar(caminho);

builder.Services.AddSingleton<IRepositorioDeSolicitacoes>(_ =>
    new RepositorioEmMemoria(dados));
builder.Services.AddScoped<INumerador, NumeradorDoBanco>();
builder.Services.AddSingleton<INotificador, NotificadorConsole>();
builder.Services.AddScoped<Balcao>();

var conexao = builder.Configuration.GetConnectionString("Principal");
builder.Services.AddDbContext<PrefeituraDbContext>(opcoes =>
    opcoes.UseNpgsql(conexao).UseSnakeCaseNamingConvention());

var app = builder.Build();

app.MapGet("/api/solicitacoes", (IRepositorioDeSolicitacoes repo) =>
    repo.Todas().Take(50));

app.MapGet("/api/solicitacoes/{id:int}",
    (int id, IRepositorioDeSolicitacoes repo) =>
    {
        var s = repo.PorId(id);
        return s is null ? Results.NotFound() : Results.Ok(s);
    });

app.MapPost("/api/solicitacoes/{id:int}/protocolo",
    (int id, HttpContext http, IRepositorioDeSolicitacoes repo,
     Balcao balcao, ILogger<Program> logger) =>
    {
        var origem = http.Request.Headers["X-Cliente"].ToString();
        using var escopo = logger.BeginScope(
            "Cliente {Cliente}, pedido {PedidoId}",
            origem, http.TraceIdentifier);

        var s = repo.PorId(id);
        if (s is null)
        {
            return Results.NotFound();
        }
        balcao.Protocolar(s);
        return Results.Ok(new { protocolo = s.Protocolo!.ToString() });
    });

app.MapGet("/api/secretarias", (PrefeituraDbContext db) =>
    db.Secretarias
        .OrderBy(s => s.Nome)
        .Select(s => new { s.Sigla, s.Nome })
        .ToList());

app.MapGet("/api/banco/solicitacoes/{id:int}",
    (int id, PrefeituraDbContext db) =>
        db.Solicitacoes
            .Include(s => s.Solicitante)
            .Include(s => s.SecretariaAtual)
            .Include(s => s.Atendimentos)
                .ThenInclude(a => a.Quem)
            .FirstOrDefault(s => s.Id == id));

app.MapGet("/api/banco/script", (PrefeituraDbContext db) =>
    db.Database.GenerateCreateScript());

app.Run();
