# Materiais — Linux One: Terminal, shell e as ferramentas que todo dev usa todo dia

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t linux-one .
docker run --rm -it -v "${PWD}:/projeto" linux-one bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/19-o-primeiro-script/checar.sh`

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `19-o-primeiro-script` | `checar.sh`, `tanque.sh`, `disco-ok.sh` |
| `20-decisoes-e-repeticoes` | `alerta-tanques.sh` |
| `21-scripts-que-nao-quebram` | `arquivar-v1.sh`, `arquivar.sh` |
| `25-agendar-tarefas` | `vigia.sh` |
| `28-compactar-e-backup` | `backup-loja.sh` |
| `35-quarta-seis-de-outubro` | `migracao.txt` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
