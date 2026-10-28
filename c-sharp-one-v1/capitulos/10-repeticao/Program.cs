int[] usados = [4211, 4212, 4213, 4214, 4215, 4217];

var candidato = 4211;
while (Array.IndexOf(usados, candidato) >= 0)
{
    candidato++;
}

Console.WriteLine($"Próximo livre: {candidato}");
