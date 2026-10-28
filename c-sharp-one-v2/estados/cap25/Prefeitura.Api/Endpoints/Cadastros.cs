using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Prefeitura.Dominio;
using Prefeitura.Infraestrutura;

namespace Prefeitura.Api.Endpoints;

public static class Cadastros
{
    public static void MapCadastros(this IEndpointRouteBuilder app)
    {
        app.MapPost("/api/cidadaos", CriarCidadao)
            .WithTags("Cadastros")
            .ProducesValidationProblem();
        app.MapGet("/api/secretarias", ListarSecretarias)
            .WithTags("Cadastros");
        app.MapPost("/api/sessoes", EntrarAsync)
            .WithTags("Sessões")
            .AllowAnonymous();
    }

    private static Created<CidadaoCriado> CriarCidadao(
        NovoCidadao pedido, PrefeituraDbContext db)
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
    }

    private static List<SecretariaResposta> ListarSecretarias(
        PrefeituraDbContext db) =>
        db.Secretarias
            .OrderBy(s => s.Nome)
            .Select(s => new SecretariaResposta(s.Sigla, s.Nome))
            .ToList();

    private static async Task<Results<Ok<Sessao>, UnauthorizedHttpResult>>
        EntrarAsync(
            Login pedido, PrefeituraDbContext db, EmissorDeTokens emissor,
            CancellationToken cancelamento)
    {
        var credencial = await db.Credenciais
            .FindAsync([pedido.Matricula], cancelamento);
        var conferida = credencial is not null
            && new PasswordHasher<Credencial>().VerifyHashedPassword(
                credencial, credencial.HashDaSenha, pedido.Senha)
               != PasswordVerificationResult.Failed;
        if (!conferida)
        {
            return TypedResults.Unauthorized();
        }
        var servidor = await db.Servidores
            .Include(s => s.Pessoa)
            .FirstAsync(s => s.Matricula == pedido.Matricula,
                        cancelamento);
        var sessao = emissor.Emitir(servidor, credencial!.Papel);
        return TypedResults.Ok(sessao);
    }
}
