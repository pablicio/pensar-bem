using System.Net;
using System.Net.Http.Json;
using System.Text.Json;

namespace Prefeitura.Api.Testes;

public class SolicitacoesTestes(ApiDaPrefeitura api)
    : IClassFixture<ApiDaPrefeitura>
{
    [Fact]
    public async Task Sem_chave_responde_401()
    {
        var resposta = await api.CreateClient()
            .GetAsync("/api/solicitacoes");

        Assert.Equal(HttpStatusCode.Unauthorized, resposta.StatusCode);
    }

    [Fact]
    public async Task Chave_do_aplicativo_nao_serve_para_cancelar()
    {
        var resposta = await api.ClienteDoAplicativo()
            .PostAsync("/api/solicitacoes/1/cancelamento", null);

        Assert.Equal(HttpStatusCode.Unauthorized, resposta.StatusCode);
        Assert.Equal("Bearer",
            resposta.Headers.WwwAuthenticate.Single().Scheme);
    }

    [Fact]
    public async Task Contrato_da_solicitacao_em_analise()
    {
        var json = await api.ClienteDoAplicativo()
            .GetFromJsonAsync<JsonElement>("/api/solicitacoes/2");

        string[] campos =
        [
            "id", "numeroSip", "protocolo", "assunto", "situacao",
            "secretaria", "criadaEm", "atendimentos"
        ];
        Assert.Equal(campos,
            json.EnumerateObject().Select(p => p.Name));
        Assert.Equal("EmAnalise", json.GetProperty("situacao").GetString());
    }

    [Fact]
    public async Task Situacao_desconhecida_no_filtro_responde_400()
    {
        var resposta = await api.ClienteDoAplicativo()
            .GetAsync("/api/solicitacoes?situacao=Xyz");

        Assert.Equal(HttpStatusCode.BadRequest, resposta.StatusCode);
    }

    [Fact]
    public async Task Criar_responde_201_com_endereco()
    {
        var resposta = await api.ClienteDoAplicativo().PostAsJsonAsync(
            "/api/solicitacoes",
            new { cidadaoId = 1, assunto = "PODA", secretaria = "SEOB" });

        Assert.Equal(HttpStatusCode.Created, resposta.StatusCode);
        Assert.StartsWith("/api/solicitacoes/",
            resposta.Headers.Location!.ToString());
    }
}
