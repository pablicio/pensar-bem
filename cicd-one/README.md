# Materiais — CI/CD One: Integração e entrega contínuas, com GitHub Actions, GitLab CI, CircleCI e Jenkins

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t cicd-one .
docker run --rm -it -v "${PWD}:/projeto" cicd-one bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/.github/workflows/testes.yml`

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `.github/workflows/testes.yml` |
| `03-o-caderno-do-wendel` | `scripts/deploy.sh`, `scripts/voltar.sh`, `Makefile` |
| `04-anatomia-de-um-pipeline` | `.github/workflows/api.yml` |
| `05-build-reproduzivel` | `api/requirements.txt`, `api/requirements.in`, `api/Dockerfile` |
| `06-testes-no-pipeline` | `.github/workflows/api.yml`, `api/tests/conftest.py` |
| `07-qualidade-automatica` | `.pre-commit-config.yaml`, `.github/CODEOWNERS`, `.github/pull_request_template.md` |
| `08-artefatos-e-versoes` | `api/app/rotas/versao.py` |
| `09-segredos-e-ambientes` | `api/app/config.py` |
| `10-cache-e-velocidade` | `.github/workflows/api.yml` |
| `11-conhecendo-o-github-actions` | `.github/workflows/exemplo.yml` |
| `12-workflows-de-verdade` | `.github/workflows/api.yml`, `.github/workflows/implanta-versao.yml` |
| `13-acoes-reutilizaveis-e-runners` | `.github/actions/prepara-python/action.yml`, `.github/workflows/servico-python.yml`, `.github/workflows/notificador.yml` |
| `14-o-piloto-no-github-actions` | `scripts/implanta.sh`, `scripts/fumaca.sh`, `.github/workflows/api.yml` |
| `15-conhecendo-o-gitlab-ci` | `.gitlab-ci.yml` |
| `16-o-piloto-no-gitlab-ci` | `.gitlab-ci.yml` |
| `17-conhecendo-o-circleci` | `.circleci/config.yml` |
| `18-o-piloto-no-circleci` | `.circleci/config.yml` |
| `19-conhecendo-o-jenkins` | `jenkins/casc.yaml` |
| `20-jenkinsfile` | `vars/servicoPython.groovy` |
| `21-o-piloto-no-jenkins` | `jenkins/Dockerfile`, `jenkins/plugins.txt` |
| `22-estrategias-de-deploy` | `api/app/rotas/viagens.py` |
| `23-deploy-sem-parar` | `infra/producao/compose.yaml`, `api/Dockerfile`, `api/app/rotas/saude.py`, `scripts/troca.sh` |
| `24-migracoes-de-banco` | `api/migracoes/versions/0042_avisos_atraso.py`, `api/scripts/preenche_partida.py`, `.github/workflows/api.yml` |
| `25-voltar-em-cinco-minutos` | `.github/workflows/volta.yml`, `docs/roteiros/voltar.md` |
| `26-o-app-nas-lojas` | `.github/workflows/app.yml` |
| `27-gitops-e-kubernetes` | `embarque-config/producao/api.yaml` |
| `28-seguranca-no-pipeline` | `.github/workflows/codeql.yml`, `.github/dependabot.yml` |
| `31-testes-instaveis-e-pipelines-lentos` | `api/tests/test_aviso_atraso.py` |
| `32-comparar-sem-paixao` | `docs/decisoes/0007-ferramenta-de-ci.md` |
| `a2-referencia-de-yaml` | `.github/workflows/pipeline.yml`, `.gitlab-ci.yml`, `.circleci/config.yml` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
