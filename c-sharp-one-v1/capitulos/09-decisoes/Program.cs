int diasDeAtraso = 4;

string situacao = diasDeAtraso switch
{
    <= 0 => "no prazo",
    <= 5 => "atrasado",
    _ => "crítico"
};

Console.WriteLine(situacao);
