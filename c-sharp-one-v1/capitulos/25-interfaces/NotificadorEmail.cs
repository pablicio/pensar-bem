public class NotificadorEmail : INotificador
{
    private readonly string _pastaDeSaida;

    public NotificadorEmail(string pastaDeSaida) =>
        _pastaDeSaida = pastaDeSaida;

    public void Enviar(Cidadao destinatario, string mensagem)
    {
        if (destinatario.Email is null)
        {
            return;
        }
        var arquivo = Path.Combine(_pastaDeSaida,
            $"{DateTime.Now:yyyyMMddHHmmss}-{destinatario.Id}.txt");
        File.WriteAllText(arquivo,
            $"Para: {destinatario.Email}\n\n{mensagem}");
    }
}
