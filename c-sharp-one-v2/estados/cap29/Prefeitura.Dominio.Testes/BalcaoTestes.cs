using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.Extensions.Time.Testing;
using NSubstitute;

namespace Prefeitura.Dominio.Testes;

public class NotificadorQueAnota : INotificador
{
    public List<(string Nome, string Texto)> Enviados { get; } = [];

    public Task EnviarAsync(Cidadao destinatario, string mensagem,
                            CancellationToken cancelamento)
    {
        Enviados.Add((destinatario.Nome, mensagem));
        return Task.CompletedTask;
    }
}

public class BalcaoTestes
{
    private static readonly Calendario Calendario =
        new([new(2027, 5, 27), new(2027, 6, 1)]);

    [Theory]
    [InlineData(15)]   // 15h em Brasília
    [InlineData(21)]   // 21h em Brasília: já é dia 11 em UTC
    public async Task Buraco_de_10_de_maio_vence_em_2_de_junho(
        int hora)
    {
        var balcao = NovoBalcao(new NotificadorQueAnota(), hora);
        var solicitacao = Nova("BURACO");

        await balcao.ProtocolarAsync(solicitacao, CancellationToken.None);

        Assert.Equal("NE-2027-000042", solicitacao.Protocolo!.ToString());
        Assert.Equal(new DateOnly(2027, 6, 2), solicitacao.PrazoEm);
    }

    [Fact]
    public async Task Aviso_vai_para_o_solicitante_com_numero_e_prazo()
    {
        var anota = new NotificadorQueAnota();
        var balcao = NovoBalcao(anota, 15);
        var solicitacao = Nova("BURACO");

        await balcao.ProtocolarAsync(solicitacao, CancellationToken.None);
        await balcao.AvisarAsync(solicitacao, CancellationToken.None);

        var (nome, mensagem) = Assert.Single(anota.Enviados);
        Assert.Equal("MARIA G SOUZA", nome);
        Assert.Equal(
            "Seu protocolo: NE-2027-000042. Prazo: até 02/06/2027.",
            mensagem);
    }

    [Fact]
    public async Task Aviso_com_biblioteca_de_dubles()
    {
        var notificador = Substitute.For<INotificador>();
        var balcao = NovoBalcao(notificador, 15);
        var solicitacao = Nova("BURACO");

        await balcao.ProtocolarAsync(solicitacao, CancellationToken.None);
        await balcao.AvisarAsync(solicitacao, CancellationToken.None);

        await notificador.Received(1).EnviarAsync(
            Arg.Is<Cidadao>(c => c.Nome == "MARIA G SOUZA"),
            Arg.Is<string>(m => m.Contains("NE-2027-000042")),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task Protocolo_no_feriado_conta_do_dia_util_seguinte()
    {
        // 1º de junho de 2027, 10h12, aniversário da cidade
        var instante = new DateTimeOffset(
            2027, 6, 1, 10, 12, 0, TimeSpan.FromHours(-3));
        var balcao = new Balcao(
            new Numerador(null), new NotificadorQueAnota(), Calendario,
            new FakeTimeProvider(instante.ToUniversalTime()),
            NullLogger<Balcao>.Instance);
        var solicitacao = Nova("2A VIA IPTU");

        await balcao.ProtocolarAsync(solicitacao, CancellationToken.None);

        Assert.Equal(new DateOnly(2027, 6, 3), solicitacao.PrazoEm);
    }

    private static Balcao NovoBalcao(INotificador notificador, int hora)
    {
        var brasilia = new DateTimeOffset(
            2027, 5, 10, hora, 30, 0, TimeSpan.FromHours(-3));
        return new Balcao(
            new Numerador(new Protocolo(2027, 41)), notificador,
            Calendario, new FakeTimeProvider(brasilia.ToUniversalTime()),
            NullLogger<Balcao>.Instance);
    }

    private static Solicitacao Nova(string assunto) =>
        new(new Cidadao(1, "MARIA G SOUZA"), assunto,
            new Secretaria("SEOB", "Obras"), DateTimeOffset.UtcNow);
}
