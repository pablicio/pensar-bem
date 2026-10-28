# Prefeitura — plataforma de solicitações

API da Prefeitura de Nova Esperança: cidadãos, solicitações, protocolo e
prazos. Atende o aplicativo da agência, o site da Ouvidoria e o balcão do
Protocolo Geral. Em produção desde 1º de junho de 2027.

Para operar (entregar, voltar, backup, restauração): `OPERACAO.md`.
O que sabemos que falta: `DIVIDA.md`.

## Os projetos

| Projeto | O que tem | Depende de |
|---|---|---|
| `Prefeitura.Dominio` | regras: solicitação, protocolo, prazos, calendário | nada |
| `Prefeitura.Infraestrutura` | EF Core, PostgreSQL, migrations, e-mail, SMS, importação do SIP | Domínio |
| `Prefeitura.Api` | endpoints, autenticação, configuração, comandos | os dois |
| `*.Testes` | testes de cada um | — |

Um projeto novo entra na solução quando houver um motivo que se diga numa
frase.

## A primeira vez

Precisa de: SDK do .NET 10 (a versão exata está no `global.json`) e Docker.

1. Suba o banco, as migrations e a API:

   ```
   cp .env.exemplo .env      # e preencha as três variáveis
   docker compose up -d
   ```

2. Para rodar a API fora do contêiner, grave os segredos de
   desenvolvimento (peça os valores a alguém da equipe, por canal
   seguro; eles não estão no repositório):

   ```
   cd Prefeitura.Api
   dotnet user-secrets set "Tokens:Chave" "..."   # 32 caracteres ou mais
   dotnet user-secrets set "Sms:Chave" "..."      # a de homologação
   dotnet run
   ```

3. Para ter dados, importe a exportação do SIP:
   `dotnet run -- importar` (o caminho do CSV está em `Sip:CaminhoCsv`).

## Testes

`dotnet test` na raiz. Os testes da API sobem um PostgreSQL de verdade
com Testcontainers: o Docker precisa estar rodando. O CI roda os mesmos
testes a cada push e a cada pull request; a `main` só aceita pull request
com o pipeline verde.

## Regras da equipe

- Os records do `Contratos.cs` são o contrato com a agência e a Ouvidoria.
  Mudar um deles é mudar o contrato, e se avisa antes.
- Toda recusa do domínio herda de `RegraDeNegocioException`, com um código
  novo na tabela do documento da API. Exceção genérica vira `500`.
- Configuração obrigatória falha na partida se faltar: texto com
  `Exigir`; lista com exigência própria. Nada de `?? []`.
- O que vale para todos os ambientes fica no `appsettings.json` — os
  feriados, por exemplo. Os arquivos por ambiente só têm o que muda.
- Bug que gravou dado errado: a correção inclui os dados, pelo domínio,
  com registro no histórico, e pode rodar duas vezes.

## Avisos conhecidos

- `Cannot load library libgssapi_krb5.so.2`, ao rodar o bundle de
  migrations: o Npgsql procura uma biblioteca de autenticação que a
  imagem mínima não tem e que a prefeitura não usa. É ruído.
- Datas em mensagens de teste saem no formato americano (`06/03/2027`)
  quando a máquina roda com a cultura invariante, como no contêiner.
