using static Prefeitura.Dominio.StatusSolicitacao;

namespace Prefeitura.Dominio.Testes;

public class CancelamentoTestes
{
    [Fact]
    public void Cancelar_em_analise_deixa_cancelada()
    {
        var solicitacao = Nova(EmAnalise);

        solicitacao.Cancelar();

        Assert.Equal(Cancelada, solicitacao.Situacao);
    }

    [Theory]
    [InlineData(Aberta)]
    [InlineData(EmAnalise)]
    [InlineData(EmAtendimento)]
    public void Pode_cancelar_o_que_nao_terminou(StatusSolicitacao de)
    {
        var solicitacao = Nova(de);

        solicitacao.Cancelar();

        Assert.Equal(Cancelada, solicitacao.Situacao);
    }

    [Theory]
    [InlineData(Resolvida)]
    [InlineData(Cancelada)]
    public void Nao_pode_cancelar_o_que_terminou(StatusSolicitacao de)
    {
        var solicitacao = Nova(de);

        Assert.Throws<SolicitacaoEncerradaException>(
            () => solicitacao.Cancelar());
    }

    private static Solicitacao Nova(StatusSolicitacao situacao) =>
        Solicitacao.Restaurar(
            "1/27", new Cidadao(1, "MARIA G SOUZA"), "BURACO",
            new Secretaria("SEOB", "Obras"), DateTimeOffset.UtcNow,
            situacao);
}
