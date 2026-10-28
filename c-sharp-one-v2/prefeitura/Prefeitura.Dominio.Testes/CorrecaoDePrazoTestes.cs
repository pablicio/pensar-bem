namespace Prefeitura.Dominio.Testes;

public class CorrecaoDePrazoTestes
{
    private static readonly Secretaria Fazenda = new("SEFA", "Fazenda");

    [Fact]
    public void Corrigir_prazo_deixa_registro_no_historico()
    {
        var solicitacao = new Solicitacao(
            new Cidadao(713, "JORGE M MENDES"), "2A VIA IPTU",
            Fazenda, DateTimeOffset.UtcNow);
        solicitacao.Protocolar(
            new Protocolo(2027, 622), new DateOnly(2027, 6, 2));
        var helena = new Servidor(
            "20001", new Cidadao(9, "HELENA M DUARTE"), Fazenda);

        solicitacao.CorrigirPrazo(
            new DateOnly(2027, 6, 3), helena, "feriado");
        solicitacao.CorrigirPrazo(
            new DateOnly(2027, 6, 3), helena, "feriado");

        Assert.Equal(new DateOnly(2027, 6, 3), solicitacao.PrazoEm);
        var registro = Assert.Single(solicitacao.Atendimentos);
        Assert.Equal(
            "Prazo corrigido de 02/06/2027 para 03/06/2027: feriado",
            registro.Descricao);
    }
}
