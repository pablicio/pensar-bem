using System.Text.Json;

var opcoes = new JsonSerializerOptions { WriteIndented = true };
var json = JsonSerializer.Serialize(linhas, opcoes);
File.WriteAllText("relatorio.json", json);

Console.WriteLine(json);
