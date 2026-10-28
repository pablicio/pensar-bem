var linhas = File.ReadAllLines("solicitacoes.csv");
var abertos = 0;
var invalidas = 0;

for (int i = 1; i < linhas.Length; i++)
{
    try
    {
        var campos = linhas[i].Split(';');
        if (campos[6] == "ABERTO")
        {
            abertos++;
        }
    }
    catch (IndexOutOfRangeException)
    {
        invalidas++;
        Console.WriteLine($"Linha {i + 1}: campos faltando");
    }
}

Console.WriteLine($"Abertos: {abertos}  Inválidas: {invalidas}");
