using System.Net.Http.Json;
using Prefeitura.Dominio;

namespace Prefeitura.Infraestrutura;

public class NotificadorSms(HttpClient http) : INotificador
{
    public async Task EnviarAsync(
        Cidadao destinatario, string mensagem,
        CancellationToken cancelamento)
    {
        if (destinatario.Celular is null)
        {
            return;
        }
        var corpo =
            new { Telefone = destinatario.Celular, Texto = mensagem };
        var resposta = await http.PostAsJsonAsync(
            "/v1/sms", corpo, cancelamento);
        resposta.EnsureSuccessStatusCode();
    }
}
