using System.Security.Claims;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.EntityFrameworkCore;
using Prefeitura.Dominio;
using Prefeitura.Infraestrutura;

namespace Prefeitura.Api.Endpoints;

public static class Solicitacoes
{
    public static void MapSolicitacoes(this IEndpointRouteBuilder app)
    {
        var grupo = app.MapGroup("/api/solicitacoes")
            .WithTags("Solicitações");

        grupo.MapGet("", Listar);
        grupo.MapGet("/{id:int}", Detalhar);
        grupo.MapPost("", Criar);
        grupo.MapPost("/{id:int}/protocolo", ProtocolarAsync)
            .RequireAuthorization("Protocolar")
            .ProducesProblem(StatusCodes.Status409Conflict);
        grupo.MapPost("/{id:int}/encaminhamento", Encaminhar)
            .RequireAuthorization("Atendimento");
        grupo.MapPost("/{id:int}/cancelamento", Cancelar)
            .RequireAuthorization("Gestao");
    }

    private static Pagina<SolicitacaoResumo> Listar(
        PrefeituraDbContext db, string? secretaria,
        StatusSolicitacao? situacao, int pagina = 1)
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
    }

    private static Results<Ok<SolicitacaoDetalhe>, NotFound> Detalhar(
        int id, PrefeituraDbContext db)
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
    }

    private static async Task<Results<Ok<ProtocoloEmitido>, NotFound>>
        ProtocolarAsync(
            int id, HttpContext http, PrefeituraDbContext db,
            Balcao balcao, ILogger<Program> logger,
            CancellationToken cancelamento)
    {
        using var escopo = logger.BeginScope(
            "Cliente {Cliente}", http.User.Identity?.Name);

        var s = await db.Solicitacoes
            .Include(x => x.Solicitante)
            .FirstOrDefaultAsync(x => x.Id == id, cancelamento);
        if (s is null)
        {
            return TypedResults.NotFound();
        }
        await balcao.ProtocolarAsync(s, cancelamento);
        await db.SaveChangesAsync(cancelamento);
        logger.LogInformation(
            "Protocolo gravado: {Protocolo}", s.Protocolo);
        await balcao.AvisarAsync(s, cancelamento);
        var emitido = new ProtocoloEmitido(
            s.Protocolo!.ToString(), s.PrazoEm!.Value);
        return TypedResults.Ok(emitido);
    }

    private static Results<Created<SolicitacaoResumo>, ValidationProblem>
        Criar(NovaSolicitacao pedido, PrefeituraDbContext db)
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
    }

    private static Results<NoContent, NotFound> Encaminhar(
        int id, Encaminhamento pedido, ClaimsPrincipal usuario,
        PrefeituraDbContext db)
    {
        var s = db.Solicitacoes
            .Include(x => x.SecretariaAtual)
            .FirstOrDefault(x => x.Id == id);
        var destino = db.Secretarias.Find(pedido.Destino);
        var matricula = usuario.FindFirstValue("sub");
        var quem = db.Servidores.Find(matricula);
        if (s is null || destino is null || quem is null)
        {
            return TypedResults.NotFound();
        }
        s.Encaminhar(destino, quem, pedido.Motivo);
        db.SaveChanges();
        return TypedResults.NoContent();
    }

    private static Results<NoContent, NotFound> Cancelar(
        int id, PrefeituraDbContext db)
    {
        var s = db.Solicitacoes.Find(id);
        if (s is null)
        {
            return TypedResults.NotFound();
        }
        s.Cancelar();
        db.SaveChanges();
        return TypedResults.NoContent();
    }
}
