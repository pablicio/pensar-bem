# Materiais — C# One — Volume 2: .NET de verdade

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
cd prefeitura
copy .env.exemplo .env   # PowerShell: Copy-Item .env.exemplo .env
# preencha SENHA_DO_BANCO, CHAVE_DOS_TOKENS e CHAVE_DO_SMS
docker compose up -d
dotnet test
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

## Snapshots da API

O projeto cresce capítulo a capítulo. Cada pasta em `estados/` é o código
como ele estava naquele capítulo (`cap08`, `cap09`, …). `prefeitura/` é o
projeto final. `correio/` é o serviço de e-mail de desenvolvimento.

Não copie `bin/`, `obj/` nem DLLs: `dotnet restore` baixa o que falta.

## O que tem neste pacote

- `estados/ (994 arquivos)`
- `prefeitura/ (77 arquivos)`
- `correio/ (2 arquivos)`

### Arquivos por capítulo

Os exemplos deste volume estão nas pastas de projeto listadas acima.

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
