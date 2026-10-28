Console.WriteLine(
    $"{"Secretaria",-16}{"Total",7}{"Abertos",9}{"Atraso",8}");
Console.WriteLine(new string('-', 40));

foreach (var l in linhas)
{
    Console.WriteLine(
        $"{l.Secretaria,-16}{l.Total,7}{l.Abertos,9}{l.Atrasados,8}");
}

Console.WriteLine(new string('-', 40));
Console.WriteLine($"{"Total",-16}{linhas.Sum(l => l.Total),7}");
