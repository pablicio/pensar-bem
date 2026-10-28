using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Prefeitura.Dominio;

namespace Prefeitura.Api.Testes;

public class ProducaoTestes
{
    [Fact]
    public void Producao_conhece_o_aniversario_da_cidade()
    {
        using var api = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(builder =>
            {
                builder.UseEnvironment("Production");
                builder.UseSetting("ConnectionStrings:Principal",
                    "Host=nenhum;Database=nenhum");
                builder.UseSetting(
                    "Tokens:Chave", new string('t', 32));
                builder.UseSetting("Sms:Chave", "chave-de-teste");
            });

        var calendario =
            api.Services.GetRequiredService<Calendario>();

        var prazo = calendario.PrazoFinal(
            new DateOnly(2027, 6, 1), "2A VIA IPTU");
        Assert.Equal(new DateOnly(2027, 6, 3), prazo);
    }
}
