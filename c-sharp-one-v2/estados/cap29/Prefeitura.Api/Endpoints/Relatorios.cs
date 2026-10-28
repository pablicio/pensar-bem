using Prefeitura.Dominio;
using Prefeitura.Infraestrutura;

namespace Prefeitura.Api.Endpoints;

public static class Relatorios
{
    public static void MapRelatorios(this IEndpointRouteBuilder app)
    {
        var grupo = app.MapGroup("/api/relatorios")
            .WithTags("Relatórios");

        grupo.MapGet("/abertas", Abertas);
        grupo.MapGet("/segunda", Segunda);
    }

    private static List<LinhaAberta> Abertas(
        string secretaria, PrefeituraDbContext db) =>
        db.Solicitacoes
            .Where(s => s.SecretariaAtual.Sigla == secretaria
                        && s.Situacao == StatusSolicitacao.Aberta)
            .OrderBy(s => s.CriadaEm)
            .Select(s => new LinhaAberta(
                s.NumeroSip ?? s.Id.ToString(), s.Assunto,
                s.Solicitante.Nome, s.CriadaEm))
            .ToList();

    private static List<LinhaRelatorio> Segunda(PrefeituraDbContext db) =>
        db.Solicitacoes
            .GroupBy(s => s.SecretariaAtual.Nome)
            .OrderByDescending(g => g.Count())
            .Select(g => new LinhaRelatorio(
                g.Key,
                g.Count(),
                g.Count(s =>
                    s.Situacao != StatusSolicitacao.Resolvida
                    && s.Situacao != StatusSolicitacao.Cancelada)))
            .ToList();
}
