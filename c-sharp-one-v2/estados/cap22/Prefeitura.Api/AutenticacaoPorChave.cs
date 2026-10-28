using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Options;

namespace Prefeitura.Api;

public class ClienteDaApi
{
    public string Nome { get; set; } = "";
    public string HashDaChave { get; set; } = "";
    public List<string> Papeis { get; set; } = [];
}

public class OpcoesClientes
{
    public List<ClienteDaApi> Clientes { get; set; } = [];
}

public static class Chaves
{
    public static string Nova() =>
        Convert.ToBase64String(RandomNumberGenerator.GetBytes(32));

    public static byte[] Hash(string chave) =>
        SHA256.HashData(Encoding.UTF8.GetBytes(chave));
}

public class AutenticacaoPorChave(
    IOptionsMonitor<AuthenticationSchemeOptions> opcoes,
    ILoggerFactory logs, UrlEncoder encoder,
    IOptions<OpcoesClientes> clientes)
    : AuthenticationHandler<AuthenticationSchemeOptions>(
        opcoes, logs, encoder)
{
    public const string Esquema = "ChaveDeApi";

    protected override Task<AuthenticateResult>
        HandleAuthenticateAsync()
    {
        var chave = Request.Headers["X-Chave-Api"].ToString();
        if (chave == "")
        {
            return Task.FromResult(AuthenticateResult.NoResult());
        }

        var hash = Chaves.Hash(chave);
        var cliente = clientes.Value.Clientes.FirstOrDefault(c =>
            CryptographicOperations.FixedTimeEquals(
                Convert.FromHexString(c.HashDaChave), hash));
        if (cliente is null)
        {
            return Task.FromResult(
                AuthenticateResult.Fail("Chave de API inválida."));
        }

        var declaracoes = new List<Claim>
        {
            new(ClaimTypes.Name, cliente.Nome)
        };
        declaracoes.AddRange(cliente.Papeis
            .Select(p => new Claim(ClaimTypes.Role, p)));
        var usuario = new ClaimsPrincipal(
            new ClaimsIdentity(declaracoes, Esquema));
        return Task.FromResult(AuthenticateResult.Success(
            new AuthenticationTicket(usuario, Esquema)));
    }
}
