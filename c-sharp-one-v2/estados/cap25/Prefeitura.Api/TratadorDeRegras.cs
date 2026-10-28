using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Prefeitura.Dominio;

namespace Prefeitura.Api;

public class TratadorDeRegras(IProblemDetailsService problemas)
    : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext http, Exception erro,
        CancellationToken cancelamento)
    {
        var detalhes = erro switch
        {
            RegraDeNegocioException regra => new ProblemDetails
            {
                Title = "Operação não permitida",
                Detail = regra.Message,
                Extensions = { ["codigo"] = regra.Codigo }
            },
            BadHttpRequestException pedido => new ProblemDetails
            {
                Status = pedido.StatusCode,
                Title = "Pedido inválido",
                Detail = pedido.Message
            },
            DbUpdateConcurrencyException => new ProblemDetails
            {
                Title = "Alterada por outro pedido",
                Detail = "A solicitação mudou enquanto este pedido " +
                         "era atendido. Consulte de novo.",
                Extensions = { ["codigo"] = "alterada-por-outro" }
            },
            _ => null
        };
        if (detalhes is null)
        {
            return false;
        }
        if (erro is ProtocoloRepetidoException repetido)
        {
            detalhes.Extensions["protocolo"] =
                repetido.Existente.ToString();
        }

        detalhes.Status ??= StatusCodes.Status409Conflict;
        http.Response.StatusCode = detalhes.Status.Value;
        return await problemas.TryWriteAsync(new()
        {
            HttpContext = http,
            ProblemDetails = detalhes,
            Exception = erro
        });
    }
}
