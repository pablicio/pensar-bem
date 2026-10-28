using System.Text;

Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
var windows1252 = Encoding.GetEncoding(1252);

string[] linhas = File.ReadAllLines(caminho, windows1252);
