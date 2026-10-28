using static Prefeitura.Dominio.StatusSolicitacao;

namespace Prefeitura.Dominio.Testes;

public class AtendimentoTestes
{
    [Fact]
    public void Segunda_via_vai_de_aberta_direto_para_atendimento()
    {
        var solicitacao = Solicitacao.Restaurar(
            "2/27", new Cidadao(2, "JOSÉ C PEREIRA"), "2A VIA IPTU",
            new Secretaria("SEFA", "Fazenda"), DateTimeOffset.UtcNow,
            Aberta);
        solicitacao.Protocolar(
            new Protocolo(2027, 1), new DateOnly(2027, 5, 4));

        solicitacao.IniciarAtendimento();

        Assert.Equal(EmAtendimento, solicitacao.Situacao);
    }
}
