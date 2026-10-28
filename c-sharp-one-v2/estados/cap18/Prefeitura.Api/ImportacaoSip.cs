using System.Globalization;
using System.Text;
using Prefeitura.Dominio;
using static Prefeitura.Dominio.StatusSolicitacao;

namespace Prefeitura.Api;

/// <summary>Lê a exportação do SIP (Windows-1252, ponto e vírgula).</summary>
public static class ImportacaoSip
{
    static ImportacaoSip() =>
        Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

    public static readonly Dictionary<string, string> SiglaDoSip = new()
    {
        ["OBRAS"] = "SEOB",
        ["SAÚDE"] = "SESA",
        ["EDUCAÇÃO"] = "SEED",
        ["TRANSPORTES"] = "SETR",
        ["FAZENDA"] = "SEFA",
        ["MEIO AMB"] = "SEMA",
    };

    public static List<Secretaria> SecretariasPadrao() =>
    [
        new("SEOB", "Obras"), new("SESA", "Saúde"),
        new("SEED", "Educação"), new("SETR", "Transportes"),
        new("SEFA", "Fazenda"), new("SEMA", "Meio Ambiente"),
    ];

    public static StatusSolicitacao? StatusDoSip(string texto) =>
        texto switch
        {
            "ABERTO" or "ABERTA" => Aberta,
            "EM ANALISE" or "EM ANÁLISE" => EmAnalise,
            "ATENDIMENTO" => EmAtendimento,
            "ENCERRADO" => Resolvida,
            "CANCELADO" => Cancelada,
            _ => null
        };

    public static List<Solicitacao> Carregar(
        string caminho, int encoding,
        Dictionary<string, Secretaria> secretarias,
        Dictionary<string, Cidadao> cidadaos)
    {
        var texto = File.ReadAllText(caminho, Encoding.GetEncoding(encoding));
        var resultado = new List<Solicitacao>();
        var ptBr = CultureInfo.GetCultureInfo("pt-BR");

        foreach (var linha in texto.Split('\n').Skip(1))
        {
            var c = linha.TrimEnd('\r').Split(';');
            if (c.Length != 8 || c[5] == ""
                || StatusDoSip(c[6]) is not { } situacao)
            {
                continue;
            }
            var chave = c[3] != "" ? c[3] : c[2];
            if (!cidadaos.TryGetValue(chave, out var cidadao))
            {
                cidadao = new Cidadao(0, c[2])
                {
                    Cpf = c[3] == "" ? null : c[3]
                };
                cidadaos[chave] = cidadao;
            }
            var data = DateOnly.ParseExact(c[1], "dd/MM/yy", ptBr);
            var criada = new DateTimeOffset(
                data.ToDateTime(TimeOnly.MinValue), TimeSpan.FromHours(-3))
                .ToUniversalTime();
            resultado.Add(Solicitacao.Restaurar(
                c[0], cidadao, c[5], secretarias[SiglaDoSip[c[4]]],
                criada, situacao));
        }
        return resultado;
    }
}
