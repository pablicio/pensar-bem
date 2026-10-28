using System.Diagnostics;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
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

builder.Services.AddOpenApi();
builder.Services.AddValidation();
builder.Services.AddProblemDetails();

builder.Services.AddScoped<INumerador, NumeradorDoBanco>();
var correio = builder.Configuration["Correio:Endereco"]!;
builder.Services.AddHttpClient<INotificador, NotificadorEmail>(http =>
    http.BaseAddress = new Uri(correio));
builder.Services.AddScoped<Balcao>();

var conexao = builder.Configuration.GetConnectionString("Principal");
builder.Services.AddDbContext<PrefeituraDbContext>(opcoes =>
    opcoes.UseNpgsql(conexao).UseSnakeCaseNamingConvention());

var app = builder.Build();

if (args.Length > 0 && args[0] == "importar")
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
    return;
}

app.UseStatusCodePages();

if (!app.Environment.IsProduction())
{
    app.MapOpenApi();
}

app.MapGet("/api/solicitacoes",
    (PrefeituraDbContext db, string? secretaria,
     StatusSolicitacao? situacao, int pagina = 1) =>
    {
        const int PorPagina = 20;
        var consulta = db.Solicitacoes.AsQueryable();

        if (secretaria is not null)
        {
            consulta = consulta.Where(
                s => s.SecretariaAtual.Sigla == secretaria);
        }
        if (situacao is not null)
        {
            consulta = consulta.Where(s => s.Situacao == situacao);
        }

        var total = consulta.Count();
        var itens = consulta
            .OrderByDescending(s => s.CriadaEm)
            .ThenBy(s => s.Id)
            .Skip((pagina - 1) * PorPagina)
            .Take(PorPagina)
            .Select(s => new SolicitacaoResumo(
                s.Id, s.Assunto, s.Situacao,
                s.SecretariaAtual.Nome, s.CriadaEm))
            .ToList();

        return new Pagina<SolicitacaoResumo>(total, pagina, itens);
    });

app.MapGet("/api/solicitacoes/{id:int}",
    Results<Ok<SolicitacaoDetalhe>, NotFound> (
        int id, PrefeituraDbContext db) =>
    {
        var s = db.Solicitacoes
            .Where(x => x.Id == id)
            .Select(x => new SolicitacaoDetalhe(
                x.Id, x.NumeroSip,
                x.Protocolo == null ? null : x.Protocolo.ToString(),
                x.Assunto, x.Situacao,
                new SecretariaResposta(
                    x.SecretariaAtual.Sigla, x.SecretariaAtual.Nome),
                x.CriadaEm,
                x.Atendimentos
                    .Select(a => new AtendimentoResposta(
                        a.Quando, a.Descricao))
                    .ToList()))
            .FirstOrDefault();
        return s is null
            ? TypedResults.NotFound()
            : TypedResults.Ok(s);
    });

app.MapPost("/api/solicitacoes/{id:int}/protocolo",
    async Task<Results<Ok<ProtocoloEmitido>, NotFound, ProblemHttpResult>> (
        int id, HttpContext http, PrefeituraDbContext db,
        Balcao balcao, ILogger<Program> logger,
        CancellationToken cancelamento) =>
    {
        var origem = http.Request.Headers["X-Cliente"].ToString();
        using var escopo = logger.BeginScope(
            "Cliente {Cliente}, pedido {PedidoId}",
            origem, http.TraceIdentifier);

        var s = await db.Solicitacoes
            .Include(x => x.Solicitante)
            .FirstOrDefaultAsync(x => x.Id == id, cancelamento);
        if (s is null)
        {
            return TypedResults.NotFound();
        }
        if (s.Protocolo is not null)
        {
            return TypedResults.Problem(
                title: "Solicitação já protocolada",
                detail: $"A solicitação {s.Id} já tem o protocolo " +
                        $"{s.Protocolo}.",
                statusCode: StatusCodes.Status409Conflict,
                extensions: new Dictionary<string, object?>
                {
                    ["protocolo"] = s.Protocolo.ToString()
                });
        }
        await balcao.ProtocolarAsync(s, cancelamento);
        await db.SaveChangesAsync(cancelamento);
        logger.LogInformation(
            "Protocolo gravado: {Protocolo}", s.Protocolo);
        var emitido = new ProtocoloEmitido(s.Protocolo!.ToString());
        return TypedResults.Ok(emitido);
    })
    .ProducesProblem(StatusCodes.Status409Conflict);

app.MapPost("/api/solicitacoes",
    Results<Created<SolicitacaoResumo>, ValidationProblem> (
        NovaSolicitacao pedido, PrefeituraDbContext db) =>
    {
        var erros = new Dictionary<string, string[]>();
        if (!Regras.Assuntos.Contains(pedido.Assunto))
        {
            erros["Assunto"] = [$"Assunto desconhecido: {pedido.Assunto}."];
        }
        var cidadao = db.Cidadaos.Find(pedido.CidadaoId);
        if (cidadao is null)
        {
            erros["CidadaoId"] = ["Cidadão não encontrado."];
        }
        var secretaria = db.Secretarias.Find(pedido.Secretaria);
        if (secretaria is null)
        {
            erros["Secretaria"] = ["Secretaria não encontrada."];
        }
        if (erros.Count > 0)
        {
            return TypedResults.ValidationProblem(erros);
        }
        var s = new Solicitacao(cidadao!, pedido.Assunto, secretaria!,
                                DateTimeOffset.UtcNow);
        db.Solicitacoes.Add(s);
        db.SaveChanges();
        var resumo = new SolicitacaoResumo(
            s.Id, s.Assunto, s.Situacao, secretaria!.Nome, s.CriadaEm);
        return TypedResults.Created($"/api/solicitacoes/{s.Id}", resumo);
    });

app.MapPost("/api/solicitacoes/{id:int}/encaminhamento",
    Results<NoContent, NotFound> (
        int id, Encaminhamento pedido, PrefeituraDbContext db) =>
    {
        var s = db.Solicitacoes
            .Include(x => x.SecretariaAtual)
            .FirstOrDefault(x => x.Id == id);
        var destino = db.Secretarias.Find(pedido.Destino);
        var quem = db.Servidores.Find(pedido.Matricula);
        if (s is null || destino is null || quem is null)
        {
            return TypedResults.NotFound();
        }
        s.Encaminhar(destino, quem, pedido.Motivo);
        db.SaveChanges();
        return TypedResults.NoContent();
    });

app.MapPost("/api/solicitacoes/{id:int}/cancelamento",
    Results<NoContent, NotFound> (int id, PrefeituraDbContext db) =>
    {
        var s = db.Solicitacoes.Find(id);
        if (s is null)
        {
            return TypedResults.NotFound();
        }
        s.Cancelar();
        db.SaveChanges();
        return TypedResults.NoContent();
    });

// TODO: só para a agência limpar os testes em homologação
app.MapDelete("/api/solicitacoes/{id:int}",
    Results<NoContent, NotFound> (int id, PrefeituraDbContext db) =>
    {
        var s = db.Solicitacoes.Find(id);
        if (s is null)
        {
            return TypedResults.NotFound();
        }
        db.Solicitacoes.Remove(s);
        db.SaveChanges();
        return TypedResults.NoContent();
    });

app.MapPost("/api/cidadaos",
    Created<CidadaoCriado> (NovoCidadao pedido, PrefeituraDbContext db) =>
{
    var c = new Cidadao(0, pedido.Nome)
    {
        Cpf = pedido.Cpf,
        Email = pedido.Email,
        Celular = pedido.Celular
    };
    db.Cidadaos.Add(c);
    db.SaveChanges();
    return TypedResults.Created(
        $"/api/cidadaos/{c.Id}", new CidadaoCriado(c.Id));
})
.ProducesValidationProblem();

app.MapGet("/api/secretarias", (PrefeituraDbContext db) =>
    db.Secretarias
        .OrderBy(s => s.Nome)
        .Select(s => new SecretariaResposta(s.Sigla, s.Nome))
        .ToList());

app.MapGet("/api/relatorios/abertas",
    (string secretaria, PrefeituraDbContext db) =>
        db.Solicitacoes
            .Where(s => s.SecretariaAtual.Sigla == secretaria
                        && s.Situacao == StatusSolicitacao.Aberta)
            .OrderBy(s => s.CriadaEm)
            .Select(s => new LinhaAberta(
                s.NumeroSip ?? s.Id.ToString(), s.Assunto,
                s.Solicitante.Nome, s.CriadaEm))
            .ToList());

app.MapGet("/api/relatorios/segunda", (PrefeituraDbContext db) =>
    db.Solicitacoes
        .GroupBy(s => s.SecretariaAtual.Nome)
        .OrderByDescending(g => g.Count())
        .Select(g => new LinhaRelatorio(
            g.Key,
            g.Count(),
            g.Count(s =>
                s.Situacao != StatusSolicitacao.Resolvida
                && s.Situacao != StatusSolicitacao.Cancelada)))
        .ToList());

app.Run();
