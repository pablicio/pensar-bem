public static class Comprovante
{
    public static string Texto(Solicitacao s, int prazoDias) => $"""
        PREFEITURA DE NOVA ESPERANÇA
        Protocolo: {s.Protocolo}
        Assunto: {s.Assunto}
        Prazo: {prazoDias} dias úteis
        """;
}
