# Materiais — SQL One: Perguntas certas para bancos de verdade

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker compose up -d
docker exec -it santarita psql -U postgres
# no psql: CREATE DATABASE santarita;  \c santarita
#          \i /dados/esquema.sql
#          \i /dados/santarita.sql
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/a1-a-base-da-santa-rita/dados/esquema.sql`

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `docker-compose.yml`
- `dados/`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `a1-a-base-da-santa-rita` | `dados/esquema.sql`, `dados/santarita.sql`, `dados/bemestar.sql`, `dados/itens_be.csv`, `dados/mysql/esquema.sql` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
