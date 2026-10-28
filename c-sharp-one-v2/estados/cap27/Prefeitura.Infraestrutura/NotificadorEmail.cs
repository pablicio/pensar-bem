using System.Net.Http.Json;
using Prefeitura.Dominio;

namespace Prefeitura.Infraestrutura;

public class NotificadorEmail(HttpClient http) : INotificador
{
    public async Task EnviarAsync(Cidadao destinatario, string mensagem,
                                  CancellationToken cancelamento)
    {
        if (destinatario.Email is null)
        {
            return;
        }
        var corpo =
            new { Para = destinatario.Email, Texto = mensagem };
        var resposta = await http.PostAsJsonAsync(
            "/mensagens", corpo, cancelamento);
        resposta.EnsureSuccessStatusCode();
    }
}
