# Materiais — Cloud One: Fundamentos de nuvem, com AWS, Google Cloud, Azure e DigitalOcean

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t cloud-one .
docker run --rm -it -v "${PWD}:/projeto" cloud-one bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/05-maquinas-virtuais/cloud-init.yaml`

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `05-maquinas-virtuais` | `cloud-init.yaml` |
| `09-kubernetes` | `api.yaml` |
| `10-funcoes-serverless` | `index.js` |
| `17-armazenamento-de-objetos` | `ciclo.json` |
| `19-cache-filas-e-nosql` | `programacao.js` |
| `21-identidade-e-acesso` | `politica-api.json` |
| `23-infraestrutura-como-codigo` | `main.tf` |
| `31-o-piloto-na-aws` | `rede.tf`, `api.tf`, `escala.tf` |
| `34-o-piloto-no-google-cloud` | `banco.tf` |
| `39-o-piloto-na-digitalocean` | `app.yaml` |
| `42-migrar` | `corte.txt` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
