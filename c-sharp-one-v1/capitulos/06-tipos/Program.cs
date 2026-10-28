using System.Globalization;

var ptBr = CultureInfo.GetCultureInfo("pt-BR");

decimal taxa = decimal.Parse("12,50", ptBr);
Console.WriteLine(taxa);
