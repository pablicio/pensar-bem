# Materiais — PHP One — Volume 1: Fundamentos do PHP

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t php-one-v1 .
docker run --rm -it -v "${PWD}:/projeto" php-one-v1 bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/multa.php`

```bash
php multa.php
```

## Projeto final

`projeto-final/` junta a última versão completa de cada arquivo do
sistema que o livro constrói. Recortes didáticos ficam só em
`capitulos/`. Como executar: abra `projeto-final/README.md`.

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `projeto-final/ (27 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `multa.php` |
| `03-primeiro-programa` | `ola.php`, `comentarios.php`, `saida.php`, `quebrado.php` |
| `04-variaveis-e-tipos` | `primeiras.php`, `tipos.php`, `aspas.php`, `chaves.php`, `tres_afirmacoes.php`, `o_defeito.php`, `tres_perguntas.php`, `explicito.php`, `constantes.php` |
| `05-conversao-automatica` | `login.php`, `casts.php`, `por_que_nao_float.php`, `dinheiro.php` |
| `06-operadores` | `aritmetica.php`, `divisoes.php`, `incremento.php`, `concatenar.php`, `composta.php`, `coalescencia.php`, `ternario.php`, `nave.php`, `atraso.php` |
| `07-condicionais` | `emprestimo.php`, `situacao.php`, `situacao_invertida.php`, `pode_emprestar.php`, `match.php`, `match_condicional.php` |
| `08-arrays` | `lista.php`, `acrescentar.php`, `mapa.php`, `dois_usos.php`, `a_regra.php`, `o_filtro_da_sexta.php`, `o_conserto.php`, `existe.php`, `copia.php`, `acervo.php`, `desempacotar.php`, `juntar.php` |
| `09-repeticoes` | `listar.php`, `com_chave.php`, `for.php`, `while.php`, `controle.php`, `acumulador.php`, `prontos.php`, `relatorio_lento.php`, `relatorio_rapido.php` |
| `10-funcoes` | `multa.php`, `chamadas.php`, `retorno.php`, `escopo.php`, `correto.php`, `conferir_multa.php`, `closure.php`, `use.php`, `arrow.php`, `map_filter.php`, `callable.php` |
| `11-strings` | `aspas.php`, `chaves.php`, `heredoc.php`, `recibo.php`, `recibo_correto.php`, `busca.php`, `normalizar.php` |
| `12-do-arquivo-ao-banco` | `volatil.php`, `salvar.php`, `carregar.php`, `emprestar.php`, `cadastrar.php`, `listar.php`, `emprestar_com_trava.php` |
| `14-duas-tabelas-conversando` | `esquema.sql` |
| `15-pdo` | `conexao.php`, `listar.php`, `busca_do_sistema.php`, `busca_segura.php`, `nomeados.php`, `formas.php`, `cadastrar.php`, `devolver.php`, `emprestar.php`, `conexao_ruim.php`, `buscar.php` |
| `16-do-include-ao-composer` | `conexao.php`, `recibo.php`, `relatorio.php`, `funcoes2.php`, `funcoes2_NOVO_final.php`, `renovar.php`, `composer.json`, `listar.php`, `composer.lock`, `.gitignore` |
| `17-classes-e-objetos` | `chaves.php`, `Livro.php`, `catalogo.php`, `Exemplar.php`, `acervo.php`, `listar.php`, `comparar.php`, `Leitor.php`, `carrinho.php` |
| `18-namespaces-e-autoload` | `importar.php`, `Livro.php`, `composer.json`, `carregador.php`, `src/Acervo/Livro.php`, `listar.php` |
| `19-encapsulamento` | `src/Acervo/Exemplar.php`, `src/Leitores/Leitor.php`, `src/Emprestimos/Multa.php`, `contador.php` |
| `20-heranca-interfaces-e-traits` | `src/Acervo/LivroInfantil.php`, `src/Acervo/LivroReferencia.php`, `src/Circulacao/Emprestavel.php`, `src/Acervo/Exemplar.php`, `relatorio.php`, `src/Circulacao/ItemDeAcervo.php`, `src/Circulacao/RegistraHistorico.php`, `src/Acervo/Classificacao.php`, `src/Acervo/Livro.php` |
| `21-excecoes` | `protegido.php`, `importar.php`, `src/Circulacao/ExemplarIndisponivel.php`, `emprestar.php`, `src/Circulacao/LimiteDeEmprestimosAtingido.php`, `sincroniza.php` |
| `22-tipagem-estrita` | `src/Acervo/Livro.php`, `multa.php`, `relatorio.php`, `src/Circulacao/Guarda.php`, `src/Emprestimos/Caixa.php`, `phpstan.neon`, `src/Emprestimos/consultas.php` |
| `23-enums-datas-e-valores` | `src/Acervo/StatusExemplar.php`, `src/Acervo/repositorio.php`, `fuso.php`, `mutavel.php`, `imutavel.php`, `src/Emprestimos/Dinheiro.php`, `src/Emprestimos/StatusEmprestimo.php`, `src/Emprestimos/PrazoDeEmprestimo.php`, `cobranca.php` |
| `24-escopo-e-referencias` | `copia.php`, `referencia.php`, `devolucoes.php`, `objeto.php`, `clone.php`, `cache.php` |
| `25-funcoes-anonimas-e-closures` | `atrasados.php`, `relatorio.php`, `filtros.php`, `combinar.php` |
| `26-manipulacao-de-arquivos` | `tudo.php`, `linha-a-linha.php`, `csv.php`, `exportar.php` |
| `27-datas-e-horarios` | `prazo.php`, `atraso.php`, `relogio.php`, `entrada.php` |
| `28-erros-e-debug` | `niveis.php`, `bootstrap.php`, `src/Registro.php` |
| `29-como-organizar-um-projeto-php` | `composer.json`, `.gitignore`, `config/app.php`, `src/funcoes.php`, `bootstrap.php`, `src/Servicos.php`, `bin/importar-doacoes.php` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
