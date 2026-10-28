public class NotificadorConsole : INotificador
{
    public void Enviar(Cidadao destinatario, string mensagem)
    {
        Console.WriteLine(
            $"[aviso para {destinatario.Nome}] {mensagem}");
    }
}
