var vistos = new HashSet<string>();
var repetidos = 0;

foreach (var numero in numerosDoCsv)
{
    if (!vistos.Add(numero))
    {
        repetidos++;
    }
}

Console.WriteLine($"Repetidos: {repetidos}");
