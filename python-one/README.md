# Materiais — Python One: Do primeiro print à API REST em produção

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t python-one .
docker run --rm -it -v "${PWD}:/projeto" python-one bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/preco.py`

```bash
python preco.py
```

## Projeto final

`projeto-final/` junta a última versão completa de cada arquivo do
sistema que o livro constrói. Recortes didáticos ficam só em
`capitulos/`. Como executar: abra `projeto-final/README.md`.

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `projeto-final/ (48 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `preco.py` |
| `03-primeiro-programa` | `ola.py`, `maioridade.py`, `produto.py` |
| `04-variaveis-e-tipos` | `tipos.py`, `por_que_nao_float.py`, `com_decimal.py`, `conversao.py`, `metodos_de_texto.py` |
| `05-operadores` | `aritmetica.py`, `estoque.py`, `faixa.py`, `logica.py`, `pertence.py`, `morsa.py` |
| `06-condicionais` | `entrada.py`, `faixa.py`, `prazo.py`, `evento.py`, `ausencia.py` |
| `07-repeticoes` | `catalogo.py`, `range.py`, `enumerate.py`, `zip.py`, `totais.py`, `reposicao.py`, `busca.py`, `pulando.py`, `for_else.py`, `comprehension.py`, `aninhado.py` |
| `08-funcoes` | `precos.py`, `chamadas.py`, `so_por_nome.py`, `defeito.py`, `correto.py`, `variaveis.py`, `kwargs.py`, `escopo.py`, `docstring.py`, `tipado.py` |
| `09-estruturas-de-dados` | `lista.py`, `fatias.py`, `ordenar.py`, `ordenar_por.py`, `tupla.py`, `desempacotar.py`, `dicionario.py`, `chave_ausente.py`, `conjunto.py`, `comprehensions.py`, `alias.py`, `copia_rasa.py` |
| `10-modulos-e-ambiente` | `precos.py`, `app.py`, `formas.py`, `padrao.py`, `requirements.txt`, `config.py` |
| `11-classes-e-objetos` | `produto.py`, `atributos.py`, `repr.py`, `eq.py`, `estoque.py` |
| `12-encapsulamento` | `produto.py`, `mangling.py`, `property.py`, `calculada.py`, `invariantes.py` |
| `13-heranca-e-protocolos` | `heranca.py`, `fundo.py`, `composicao.py`, `pato.py`, `abc.py`, `protocol.py` |
| `14-excecoes` | `conversao.py`, `o_pior_codigo.py`, `completo.py`, `arquivo.py`, `excecoes_do_projeto.py`, `from.py`, `log.py` |
| `15-tipagem-e-dataclasses` | `anotado.py`, `tipos.py`, `dataclass.py`, `post_init.py`, `frozen.py`, `status.py`, `o_que_vem_por_ai.py` |
| `16-o-que-e-fastapi` | `sem_framework.py`, `main.py` |
| `17-primeiro-projeto-fastapi` | `requirements.txt`, `.env.example`, `app/config.py`, `app/routers/produtos.py`, `app/main.py`, `ordem.py`, `cors.py`, `app/routers/produtores.py` |
| `18-primeira-api` | `app/routers/produtos.py` |
| `19-modelando-com-pydantic` | `app/schemas/produto.py`, `app/routers/produtos.py`, `o_teste.py`, `restricoes.py`, `tipos_ricos.py`, `validador.py`, `from_attributes.py`, `alias.py` |
| `20-banco-de-dados` | `criar_tabela.sql`, `as_quatro_operacoes.sql`, `transacao.sql`, `conexao_crua.py` |
| `21-sqlalchemy` | `app/database.py`, `app/models/produto.py`, `escrever.py`, `ler.py`, `alterar.py` |
| `22-repository` | `app/repositories/produto.py`, `o_vazamento.py`, `app/repositories/memoria.py` |
| `23-service` | `app/services/produto.py`, `app/routers/produtos.py`, `transacao.py`, `app/dependencies.py`, `a_corrida.py` |
| `24-o-crud-completo` | `app/dependencies.py`, `app/routers/produtos.py`, `app/services/produto.py`, `app/schemas/produto.py`, `app/main.py` |
| `25-schemas` | `app/schemas/produto.py`, `exclude_unset.py`, `app/services/produto.py`, `aninhado.py`, `alias.py`, `exemplos.py` |
| `26-validacao` | `app/schemas/produto.py`, `normalizacao.py`, `app/services/produto.py`, `restricoes.py`, `model_validator.py`, `saida.py` |
| `27-tratamento-de-erros` | `app/errors.py`, `app/main.py`, `app/routers/produtos.py`, `app/middleware.py` |
| `28-paginacao` | `app/schemas/pagina.py`, `app/routers/produtos.py`, `app/services/produto.py`, `app/repositories/produto.py`, `cursor.py` |
| `29-filtros-e-buscas` | `app/schemas/filtro.py`, `app/routers/produtos.py`, `app/repositories/produto.py`, `ordem.py`, `sem_acento.py` |
| `30-relacionamentos` | `app/models/produtor.py`, `o_defeito.py`, `selectinload.py`, `raiseload.py`, `tags.py`, `schema.py` |
| `31-migrations` | `alembic.ini`, `migracoes/env.py`, `migracoes/versions/a1b2c3_cria_produto.py`, `renomear.py`, `dados.py` |
| `32-dependency-injection` | `decorador.py`, `com_argumento.py`, `dependencia.py`, `app/dependencies.py`, `cadeia.py`, `guarda.py`, `classe.py`, `tests/conftest.py` |
| `33-async` | `laco.py`, `o_erro.py`, `httpx_cliente.py`, `paralelo.py`, `async_db.py`, `repo_async.py` |
| `34-autenticacao` | `app/security.py`, `app/models/usuario.py`, `app/schemas/usuario.py`, `app/services/usuario.py`, `app/routers/auth.py` |
| `35-jwt` | `app/security.py`, `app/dependencies.py`, `uso.py`, `renovacao.py` |
| `36-usuarios-e-permissoes` | `app/models/usuario.py`, `app/dependencies.py`, `uso.py`, `app/services/produto.py`, `listagem.py`, `auditoria.py` |
| `37-testando-python` | `tests/test_precos.py`, `tests/test_produto.py`, `tests/conftest.py`, `tests/test_frete.py` |
| `38-testando-services` | `tests/dublês.py`, `tests/test_servico_produto.py`, `tests/test_notificacao.py`, `fragil_vs_solido.py`, `tempo.py` |
| `39-testando-a-api` | `tests/test_api_produtos.py`, `tests/conftest.py`, `tests/test_api_seguranca.py`, `tests/test_auth.py`, `tests/test_contrato.py` |
| `40-testando-o-banco` | `tests/conftest.py`, `tests/test_banco.py`, `tests/test_concorrencia.py` |
| `41-openapi` | `app/main.py`, `rota_documentada.py`, `exemplos.py`, `versao.py`, `producao.py` |
| `42-git` | `.gitignore`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml` |
| `43-projeto-final` | `app/models/entrega.py`, `app/services/entrega.py`, `Dockerfile`, `compose.yaml`, `entrypoint.sh`, `app/routers/saude.py`, `app/log.py` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
