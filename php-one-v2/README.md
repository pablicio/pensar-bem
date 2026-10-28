# Materiais — PHP One — Volume 2: Acelerando com Laravel

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t php-one-v2 .
docker run --rm -it -v "${PWD}:/projeto" php-one-v2 bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/01-o-que-e-http/api.php`

```bash
php api.php
```

## Projeto final

`projeto-final/` junta a última versão completa de cada arquivo do
sistema que o livro constrói. Recortes didáticos ficam só em
`capitulos/`. Como executar: abra `projeto-final/README.md`.

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `projeto-final/ (29 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `01-o-que-e-http` | `api.php` |
| `03-um-framework-de-quarenta-linhas` | `.htaccess`, `mini.php` |
| `05-primeiro-projeto-laravel` | `routes/web.php`, `public/index.php` |
| `06-configuracao-ambiente-e-artisan` | `config/biblioteca.php`, `app/Console/Commands/FecharMultasDoDia.php`, `routes/console.php`, `app/Console/Commands/ListarAtrasados.php` |
| `07-rotas-e-controllers` | `routes/api.php`, `app/Http/Controllers/LivroController.php`, `app/Http/Controllers/DevolucaoController.php`, `app/Http/Controllers/EmprestimoController.php` |
| `08-requests-e-responses` | `app/Http/Controllers/LivroController.php`, `app/Http/Controllers/CapaController.php`, `app/Http/Controllers/EmprestimoController.php`, `app/Http/Controllers/DevolucaoController.php` |
| `09-blade` | `app/Http/Controllers/PainelController.php`, `resources/views/painel/index.blade.php`, `resources/views/components/layout.blade.php`, `resources/views/painel/emprestar.blade.php`, `resources/views/painel/devolver.blade.php`, `resources/views/components/busca-por-tombo.blade.php` |
| `10-migrations-seeders-e-factories` | `database/seeders/AssuntoSeeder.php`, `database/factories/LivroFactory.php` |
| `11-eloquent` | `app/Models/Livro.php`, `app/Providers/AppServiceProvider.php`, `app/Models/Exemplar.php`, `app/Casts/DinheiroCast.php`, `app/Models/Emprestimo.php`, `app/Models/Leitor.php` |
| `12-relacionamentos` | `app/Models/Livro.php`, `app/Models/Exemplar.php`, `app/Http/Controllers/AcervoController.php`, `app/Providers/AppServiceProvider.php` |
| `13-o-crud-completo` | `routes/api.php`, `app/Http/Controllers/LivroController.php`, `app/Http/Controllers/EmprestimoController.php`, `app/Http/Controllers/ExemplarController.php` |
| `14-validation-e-form-requests` | `app/Http/Controllers/LivroController.php`, `app/Http/Requests/StoreLivroRequest.php`, `app/Http/Requests/UpdateLivroRequest.php`, `app/Rules/Isbn13.php`, `app/Http/Requests/RealizarEmprestimoRequest.php`, `app/Http/Requests/StoreLeitorRequest.php` |
| `15-api-resources` | `app/Http/Resources/LeitorResource.php`, `app/Http/Controllers/LeitorController.php`, `app/Http/Controllers/LivroController.php`, `app/Http/Resources/LivroResource.php`, `app/Http/Resources/EmprestimoResource.php` |
| `16-paginacao-filtros-e-buscas` | `app/Http/Requests/ListarLivrosRequest.php`, `app/Acervo/FiltroDeLivros.php`, `app/Models/Livro.php`, `app/Http/Controllers/LivroController.php` |
| `17-erros-padronizados` | `bootstrap/app.php`, `app/Http/RespostaDeErro.php`, `app/Emprestimos/ExcecaoDeDominio.php`, `app/Emprestimos/ExemplarIndisponivel.php`, `app/Support/Incidente.php`, `app/Emprestimos/LeitorComPendencia.php` |
| `18-service-container` | `app/Http/Controllers/EmprestimoController.php`, `app/Providers/AvisoServiceProvider.php`, `app/Avisos/EnviadorDeAviso.php`, `app/Avisos/EnviadorNoLog.php`, `tests/Feature/EmprestimoTest.php`, `tests/Fakes/EnviadorFalso.php`, `app/Avisos/LembreteDeDevolucao.php` |
| `19-services` | `app/Emprestimos/EmprestimoService.php`, `app/Emprestimos/RegrasDeCirculacao.php`, `app/Emprestimos/Autorizacao.php`, `app/Http/Controllers/EmprestimoController.php` |
| `20-middleware` | `app/Http/Middleware/MedeTempo.php`, `bootstrap/app.php`, `routes/api.php`, `app/Http/Middleware/ForcaJson.php`, `app/Http/Middleware/RegistraRequisicao.php`, `app/Providers/AppServiceProvider.php`, `app/Http/Middleware/ExigeVersaoMinima.php` |
| `21-autenticacao` | `app/Auth/ConferidorDeSenha.php`, `app/Models/Usuario.php`, `app/Auth/Papel.php`, `app/Http/Controllers/Auth/LoginController.php`, `routes/api.php`, `app/Http/Controllers/EuController.php`, `app/Http/Controllers/Auth/LogoutController.php`, `app/Http/Controllers/TrocaDeSenhaController.php`, `app/Http/Requests/TrocaDeSenhaRequest.php` |
| `22-autorizacao` | `app/Providers/AppServiceProvider.php`, `app/Policies/EmprestimoPolicy.php`, `app/Http/Controllers/EmprestimoController.php`, `app/Http/Requests/RealizarEmprestimoRequest.php`, `app/Models/Emprestimo.php`, `app/Policies/LivroPolicy.php`, `app/Auth/Papel.php`, `tests/Feature/EmprestimoAutorizacaoTest.php`, `app/Policies/LeitorPolicy.php`, `app/Http/Requests/UpdateLeitorRequest.php` |
| `23-events-jobs-e-filas` | `app/Emprestimos/Eventos/EmprestimoRealizado.php`, `app/Emprestimos/EmprestimoService.php`, `app/Listeners/EnviarComprovanteDeEmprestimo.php`, `app/Jobs/AvisarDevolucaoProxima.php`, `routes/console.php`, `app/Emprestimos/Eventos/ExemplarDevolvido.php`, `app/Listeners/AvisarReservaDisponivel.php` |
| `24-cache-logs-e-medicao` | `app/Providers/AppServiceProvider.php`, `app/Acervo/MaisEmprestados.php`, `app/Listeners/EsquecerMaisEmprestados.php`, `config/logging.php` |
| `25-testes` | `tests/Unit/DinheiroTest.php`, `tests/Unit/PrazoDeEmprestimoTest.php`, `app/Emprestimos/SituacaoDoPedido.php`, `app/Emprestimos/PoliticaDeEmprestimo.php`, `tests/Unit/PoliticaDeEmprestimoTest.php`, `tests/Unit/ExemplarTest.php`, `tests/Unit/DevolucaoDaCaixaTest.php` |
| `26-testes-de-feature-http-e-banco` | `tests/Feature/LivroTest.php`, `tests/Pest.php`, `phpunit.xml`, `tests/Feature/ProtecaoTest.php`, `tests/Feature/EmprestimoAutorizacaoTest.php`, `tests/Feature/CamposInternosTest.php`, `tests/Feature/EmprestimoFluxoTest.php` |
| `27-documentacao-da-api` | `app/Http/Controllers/EmprestimoController.php`, `tests/Feature/ContratoTest.php`, `app/Http/Resources/EmprestimoResource.php` |
| `28-git-ci-e-deploy` | `.gitignore`, `.github/workflows/esteira.yml`, `deploy.sh`, `app/Http/Controllers/ProntoController.php` |
| `29-upload-de-arquivos` | `app/Http/Requests/CapaRequest.php`, `app/Http/Resources/LivroResource.php`, `app/Http/Controllers/TermoDeDoacaoController.php`, `app/Http/Controllers/CapaController.php`, `app/Jobs/PrepararCapa.php`, `tests/Feature/CapaTest.php` |
| `30-mail-e-notificacoes` | `app/Models/Leitor.php`, `app/Notifications/DevolucaoAmanha.php`, `routes/console.php`, `app/Notifications/Canais/CanalWhatsApp.php`, `lang/pt_BR.json`, `app/Mail/TermoDeDoacaoAssinado.php`, `tests/Feature/AvisoDeDevolucaoTest.php` |
| `31-queues-na-pratica` | `routes/console.php`, `app/Providers/AppServiceProvider.php`, `app/Notifications/DevolucaoAmanha.php`, `app/Importacao/ImportarDoacoes.php`, `app/Jobs/ImportarLote.php`, `app/Http/Controllers/ImportacaoController.php`, `app/Jobs/GerarRelatorioMensal.php`, `config/queue.php` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
