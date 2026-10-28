static void ProtocolarNoBalcao(
    Solicitacao s, List<Solicitacao> todas)
{
    var ultimo = todas
        .Where(x => x.Protocolo is not null)
        .Max(x => x.Protocolo!.Sequencial);
    var protocolo = new Protocolo(2027, ultimo + 1);
    s.Protocolar(protocolo);

    var texto = $"""
        PREFEITURA DE NOVA ESPERANÇA
        Protocolo: {protocolo}
        Assunto: {s.Assunto}
        Prazo: {Regras.PrazoEmDias(s.Assunto)} dias úteis
        """;
    File.WriteAllText($"comprovante-{protocolo}.txt", texto);

    var celular = s.Solicitante.Celular ?? "(sem celular)";
    Console.WriteLine($"[SMS para {celular}] Protocolo: {protocolo}");
}
