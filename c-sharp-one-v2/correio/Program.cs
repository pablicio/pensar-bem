// Correio falso, só para os testes do livro: aceita uma mensagem e
// demora o que estiver em CORREIO_DEMORA_MS (padrão 4000) para responder.
var app = WebApplication.CreateBuilder(args).Build();
var demora = int.Parse(
    Environment.GetEnvironmentVariable("CORREIO_DEMORA_MS") ?? "4000");
var recebidas = 0;
app.MapPost("/mensagens", async (HttpRequest pedido) =>
{
    var corpo = await new StreamReader(pedido.Body).ReadToEndAsync();
    File.AppendAllText("/tmp/mensagens.txt", corpo + "\n");
    await Task.Delay(demora);
    Interlocked.Increment(ref recebidas);
    return Results.Accepted();
});
var sms = 0;
app.MapPost("/v1/sms", async (HttpRequest pedido) =>
{
    var corpo = await new StreamReader(pedido.Body).ReadToEndAsync();
    File.AppendAllText("/tmp/mensagens.txt", "sms " + corpo + "\n");
    if (pedido.Headers.Authorization.ToString() != "Bearer sms-teste")
    {
        return Results.Unauthorized();
    }
    Interlocked.Increment(ref sms);
    return Results.Accepted();
});
app.MapGet("/contagem", () => recebidas);
app.MapGet("/contagem-sms", () => sms);
app.Run("http://0.0.0.0:5200");
