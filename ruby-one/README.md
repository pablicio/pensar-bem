# Materiais — Ruby One: Do primeiro puts ao contrato em produção

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t ruby-one .
docker run --rm -it -v "${PWD}:/projeto" ruby-one bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/contrato.rb`

```bash
ruby contrato.rb
```

## Projeto final

`projeto-final/` junta a última versão completa de cada arquivo do
sistema que o livro constrói. Recortes didáticos ficam só em
`capitulos/`. Como executar: abra `projeto-final/README.md`.

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `projeto-final/ (38 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `contrato.rb` |
| `03-primeiro-programa` | `contrato.rb`, `quebra.rb`, `nome.rb` |
| `04-objetos-e-tipos` | `diarias.rb`, `proporcional.rb` |
| `05-metodos` | `app/models/contract.rb`, `ativo.rb` |
| `06-condicionais` | `app/reports/ocupacao.rb`, `situacao.rb`, `ocupacao.rb`, `app/controllers/contracts_controller.rb` |
| `07-strings-e-simbolos` | `linha.rb`, `reais.rb` |
| `08-arrays-e-hashes` | `normalizar.rb` |
| `09-blocos-e-enumerables` | `bloco.rb`, `manha.rb` |
| `10-classes` | `contrato.rb`, `dois.rb` |
| `11-modulos` | `app/models/reservation.rb`, `billable.rb`, `contrato.rb`, `reserva.rb`, `patio.rb` |
| `12-excecoes` | `lista.rb`, `erros.rb`, `reservar.rb` |
| `13-gems-e-bundler` | `planilha.rb`, `Gemfile`, `Gemfile.lock` |
| `15-modelos` | `app/models/contract.rb`, `app/models/application_record.rb`, `db/schema.rb`, `config/initializers/inflections.rb` |
| `16-migrations` | `db/migrate/20211119170200_add_started_at_to_contracts.rb`, `db/migrate/20260406140000_add_site_code_to_contracts.rb`, `db/migrate/20260406160000_backfill_contract_status.rb`, `db/migrate/20260406170000_require_contract_status.rb`, `db/migrate/20260406150000_add_comments_to_contract_dates.rb` |
| `17-associacoes` | `app/models/equipment.rb`, `app/models/contract.rb` |
| `18-validacoes` | `app/models/contract.rb`, `config/locales/pt-BR.yml` |
| `19-callbacks` | `app/models/contract.rb`, `script/reproduzir_reserva_dupla.rb` |
| `20-rotas` | `config/routes.rb` |
| `21-controllers` | `app/controllers/contracts_controller.rb` |
| `22-views` | `app/views/contracts/_linha.html.erb`, `app/views/contracts/index.html.erb`, `app/models/contract.rb`, `app/helpers/contracts_helper.rb`, `app/views/contracts/new.html.erb` |
| `24-testes` | `spec/factories/contracts.rb`, `spec/models/contract_spec.rb`, `spec/models/equipment_spec.rb` |
| `25-jobs` | `app/jobs/notify_helena_job.rb`, `config/application.rb`, `app/models/contract.rb`, `app/jobs/notify_serra_azul_job.rb` |
| `26-apis` | `app/models/contract.rb`, `config/routes.rb`, `app/controllers/api/v1/contracts_controller.rb` |
| `27-autenticacao` | `app/models/user.rb`, `app/controllers/sessions_controller.rb`, `app/controllers/application_controller.rb`, `app/models/api_credential.rb`, `app/controllers/api/base_controller.rb`, `app/controllers/api/contracts_controller.rb`, `app/controllers/api/v1/contracts_controller.rb`, `spec/requests/api/contracts_spec.rb` |
| `28-deploy` | `.github/workflows/ci.yml` |
| `29-projeto-final` | `app/controllers/occupancy_controller.rb`, `app/models/contract.rb`, `spec/models/contract_spec.rb` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
