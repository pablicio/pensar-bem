using Microsoft.Extensions.Logging.Abstractions;

namespace Prefeitura.Dominio.Testes;

public class NotificadorQueFalha : INotificador
{
    public Task EnviarAsync(Cidadao destinatario, string mensagem,
                            CancellationToken cancelamento) =>
        throw new HttpRequestException("serviço fora do ar");
}

public class NotificadorMultiploTestes
{
    [Fact]
    public async Task Um_canal_que_falha_nao_impede_os_outros()
    {
        var anota = new NotificadorQueAnota();
        var multiplo = new NotificadorMultiplo(
            NullLogger<NotificadorMultiplo>.Instance,
            new NotificadorQueFalha(), anota);

        await multiplo.EnviarAsync(
            new Cidadao(1, "MARIA G SOUZA"), "Seu protocolo: X",
            CancellationToken.None);

        Assert.Single(anota.Enviados);
    }
}
