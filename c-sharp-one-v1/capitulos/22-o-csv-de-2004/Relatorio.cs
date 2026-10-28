using (var saida =
           new StreamWriter("relatorio.csv", false, Encoding.UTF8))
{
    saida.WriteLine("Secretaria;Total;Abertos;Atrasados");
    foreach (var l in linhas)
    {
        saida.WriteLine(
            $"{l.Secretaria};{l.Total};{l.Abertos};{l.Atrasados}");
    }
}
