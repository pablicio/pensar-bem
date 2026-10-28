public void Protocolar(Solicitacao s)
{
    var protocolo = _numerador.Proximo();
    s.Protocolar(protocolo);

    var texto = Comprovante.Texto(s, Regras.PrazoEmDias(s.Assunto));
    File.WriteAllText($"comprovante-{protocolo}.txt", texto);

    Console.WriteLine($"[SMS] Seu protocolo: {protocolo}");
}
