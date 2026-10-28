# Materiais — Docker One: Da minha máquina à produção, sem mistério

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t docker-one .
docker run --rm -it -v "${PWD}:/projeto" docker-one bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/09-dentro-do-container/index.html`

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `09-dentro-do-container` | `index.html` |
| `15-o-primeiro-dockerfile` | `api/main.py`, `api/requirements.txt`, `api/Dockerfile` |
| `16-cmd-e-entrypoint` | `api/entrypoint.sh`, `api/Dockerfile` |
| `17-expose-env-arg-e-user` | `api/Dockerfile` |
| `18-camadas-cache-e-contexto` | `site/Dockerfile`, `site/.dockerignore` |
| `19-multi-stage` | `api/requirements.txt`, `api/Dockerfile` |
| `20-tags-e-versoes` | `api/Dockerfile` |
| `28-compose` | `compose.yaml` |
| `29-build-redes-e-volumes-no-compose` | `compose.yaml` |
| `30-variaveis-e-arquivos-env` | `compose.yaml`, `.env.exemplo` |
| `31-dependencias-e-healthchecks` | `compose.yaml`, `api/saude.py`, `api/Dockerfile` |
| `32-profiles-ambientes-e-escala` | `compose.yaml`, `compose.override.yaml`, `compose.prod.yaml` |
| `33-tarefas-logs-e-atualizacoes` | `compose.yaml` |
| `34-a-api-em-fastapi` | `api/config.py`, `api/main.py`, `banco/01-reservas.sql`, `compose.yaml` |
| `35-node-e-php` | `checkin/server.js`, `checkin/package.json`, `checkin/Dockerfile`, `site/Dockerfile`, `site/php/serra.ini` |
| `36-java-e-spring-boot` | `fiscal/Dockerfile`, `fiscal/src/main/resources/application.properties`, `compose.yaml` |
| `37-postgresql-e-redis` | `api/assentos.py`, `compose.yaml`, `api/banco.py` |
| `38-hot-reload-e-testes` | `compose.override.yaml`, `api/tests/test_reservas.py`, `api/Dockerfile`, `compose.testes.yaml` |
| `39-migrations` | `api/migracoes/env.py`, `api/migracoes/versions/0002_meia_entrada.py`, `compose.yaml` |
| `41-versoes-promocao-e-erros` | `compose.prod.yaml` |
| `42-github-actions` | `.github/workflows/api.yml` |
| `43-deploy-e-rollback` | `.github/workflows/api.yml` |
| `45-caddy-e-https` | `Caddyfile`, `compose.prod.yaml` |
| `46-segredos-saude-e-limites` | `compose.prod.yaml`, `api/config.py` |
| `47-observar` | `compose.prod.yaml` |
| `48-atualizar-e-sobreviver` | `compose.prod.yaml` |
| `49-o-container-nao-e-uma-cela` | `compose.prod.yaml` |
| `54-o-ambiente-inteiro` | `compose.yaml`, `compose.override.yaml` |
| `55-do-push-ao-https` | `compose.prod.yaml` |
| `56-o-ensaio-de-falha` | `carga.js`, `Caddyfile` |
| `a2-dockerfile` | `.dockerignore` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
