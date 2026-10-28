using System.Security.Claims;
using System.Text;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.JsonWebTokens;
using Microsoft.IdentityModel.Tokens;
using Prefeitura.Dominio;

namespace Prefeitura.Api;

public class OpcoesTokens
{
    public string Emissor { get; set; } = "";
    public string Publico { get; set; } = "";
    public string Chave { get; set; } = "";
    public int HorasDeValidade { get; set; } = 8;

    public SymmetricSecurityKey ChaveDeAssinatura() =>
        new(Encoding.UTF8.GetBytes(Chave));
}

public record Login(string Matricula, string Senha);

public record Sessao(string Token, DateTime ExpiraEm);

public class EmissorDeTokens(IOptions<OpcoesTokens> opcoes)
{
    public Sessao Emitir(Servidor servidor, string papel)
    {
        var o = opcoes.Value;
        var expira = DateTime.UtcNow.AddHours(o.HorasDeValidade);
        var descricao = new SecurityTokenDescriptor
        {
            Issuer = o.Emissor,
            Audience = o.Publico,
            Expires = expira,
            Subject = new ClaimsIdentity(
            [
                new Claim("sub", servidor.Matricula),
                new Claim("name", servidor.Pessoa.Nome),
                new Claim("role", papel),
            ]),
            SigningCredentials = new SigningCredentials(
                o.ChaveDeAssinatura(), SecurityAlgorithms.HmacSha256),
        };
        var token = new JsonWebTokenHandler().CreateToken(descricao);
        return new Sessao(token, expira);
    }
}
