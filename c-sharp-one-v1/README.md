# Materiais — C# One — Volume 1: Fundamentos de C#

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t csharp-one-v1 .
docker run --rm -it -v "${PWD}:/projeto" csharp-one-v1 bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/Program.cs`

No volume 1, crie o projeto `dotnet new console` e substitua `Program.cs`.
No volume 2, abra o snapshot em `estados/cap08` com `dotnet run --project Prefeitura.Api`.

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `Program.cs` |
| `03-afinal-o-que-e-csharp` | `global.json` |
| `04-o-primeiro-programa` | `Protocolo.csproj`, `Program.cs` |
| `05-variaveis` | `Program.cs` |
| `06-tipos` | `Program.cs` |
| `07-null` | `Program.cs` |
| `08-strings` | `Program.cs` |
| `09-decisoes` | `Program.cs` |
| `10-repeticao` | `Program.cs` |
| `11-metodos` | `Program.cs` |
| `12-excecoes` | `Program.cs` |
| `13-o-cidadao-vira-um-objeto` | `Cidadao.cs`, `Program.cs` |
| `14-encapsulamento` | `Solicitacao.cs`, `Program.cs` |
| `15-enums` | `StatusSolicitacao.cs`, `Csv.cs`, `Solicitacao.cs` |
| `16-records` | `Protocolo.cs`, `Program.cs` |
| `17-criando-o-dominio` | `Secretaria.cs`, `Servidor.cs`, `Atendimento.cs`, `Solicitacao.cs`, `Program.cs` |
| `18-colecoes` | `Program.cs`, `Importacao.cs` |
| `19-lambdas` | `Filtros.cs`, `Program.cs` |
| `20-encontrando-cidadaos` | `Program.cs`, `Balcao.cs` |
| `21-relatorios` | `Relatorio.cs`, `LinhaRelatorio.cs` |
| `22-o-csv-de-2004` | `Importacao.cs`, `Relatorio.cs`, `Program.cs` |
| `23-datas-e-prazos` | `Csv.cs`, `Prazos.cs`, `Program.cs` |
| `24-a-reuniao-que-deu-errado` | `DIVIDA.md`, `Program.cs`, `Numerador.cs`, `Comprovante.cs`, `Balcao.cs` |
| `25-interfaces` | `INotificador.cs`, `NotificadorConsole.cs`, `NotificadorEmail.cs`, `Balcao.cs`, `Program.cs`, `NotificadorMultiplo.cs`, `NotificadorQueAnota.cs`, `Conferencia.cs` |
| `26-heranca-e-composicao` | `Pessoa.cs`, `Servidor.cs`, `Cidadao.cs`, `SolicitacaoEncerradaException.cs` |
| `27-da-pasta-a-solucao` | `Prefeitura.Dominio/Cidadao.cs`, `Protocolo/Program.cs` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
