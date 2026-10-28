using Prefeitura.Dominio;
using Prefeitura.Infraestrutura;

namespace Prefeitura.Api.Testes;

public class NotificadoresTestes
{
    [Fact]
    public async Task Sms_sem_celular_nao_avisa_e_nao_falha()
    {
        var sms = new NotificadorSms(new HttpClient());
        var semCelular = new Cidadao(1, "MARIA G SOUZA");

        await sms.EnviarAsync(
            semCelular, "Seu protocolo: X", CancellationToken.None);
    }
}
