namespace Prefeitura.Dominio.Testes;

public class ProtocoloTestes
{
    [Fact]
    public void Escreve_com_seis_digitos()
    {
        Assert.Equal("NE-2027-000014", new Protocolo(2027, 14).ToString());
    }

    [Fact]
    public void Recusa_ano_anterior_a_2027()
    {
        Assert.Throws<ArgumentOutOfRangeException>(
            () => new Protocolo(2026, 1));
    }
}
