Console.WriteLine(Regras.PrazoEmDias("PODA"));
Console.WriteLine(Regras.ExigeCpf("ALVARA"));

static class Regras
{
    public static int PrazoEmDias(string assunto) => assunto switch
    {
        "BURACO" => 15,
        "ILUMINACAO" => 10,
        "PODA" => 30,
        "2A VIA IPTU" => 1,
        _ => 30
    };

    public static bool ExigeCpf(string assunto) =>
        assunto is "2A VIA IPTU" or "ALVARA";
}
