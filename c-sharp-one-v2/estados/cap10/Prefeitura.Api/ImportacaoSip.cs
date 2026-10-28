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

    public static readonly Dictionary<string, Secretaria> Secretarias = new()
    {
        ["OBRAS"] = new("SEOB", "Obras"),
        ["SAÚDE"] = new("SESA", "Saúde"),
        ["EDUCAÇÃO"] = new("SEED", "Educação"),
        ["TRANSPORTES"] = new("SETR", "Transportes"),
        ["FAZENDA"] = new("SEFA", "Fazenda"),
        ["MEIO AMB"] = new("SEMA", "Meio Ambiente"),
    };

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
        string caminho, int encoding = 1252)
    {
        var texto = File.ReadAllText(caminho, Encoding.GetEncoding(encoding));
        var cidadaos = new Dictionary<string, Cidadao>();
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
            var id = int.Parse(c[0].Split('/')[0]);
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
                id, cidadao, c[5], Secretarias[c[4]], criada, situacao));
        }
        return resultado;
    }
}
