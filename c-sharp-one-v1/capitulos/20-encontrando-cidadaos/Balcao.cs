var palavras =
    busca.Split(' ', StringSplitOptions.RemoveEmptyEntries);

var encontrados = cidadaos
    .Where(c => palavras.All(p => Texto.Contem(c.Nome, p)))
    .OrderBy(c => c.Nome)
    .Take(20)
    .ToList();
