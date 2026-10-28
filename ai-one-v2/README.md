# Materiais — AI One — Volume 2: Programação e Dados

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t ai-one-v2 .
docker run --rm -it -v "${PWD}:/projeto" ai-one-v2 bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/ola.py`

```bash
python ola.py
```

Para o JupyterLab (caderno no navegador):

```bash
docker run --rm -it -p 8888:8888 -v "${PWD}:/projeto" ai-one-v2 jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `requirements.txt`
- `projeto/ (11 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `ola.py`, `requirements.txt`, `Dockerfile`, `versoes.py` |
| `01-r-47-mil-em-lugar-errado` | `conta.py`, `conta_v0.py`, `conta_mb.py` |
| `02-um-programa-e-um-arquivo-que-alguem-consegue-rodar-de-novo` | `total.py`, `total_v0.py`, `fator.py`, `total_trocado.py` |
| `03-um-feriado-de-natal-em-amsterda` | `zen.py`, `zen_v0.py`, `versao_minima.py`, `zen_cifrado.py` |
| `04-texto-que-parece-numero` | `numero_br.py`, `reais.py`, `checa_faixa.py` |
| `05-listas-dicionarios-e-a-pergunta-cade-o-dirceu` | `cadastro.py`, `busca.py`, `situacoes.py`, `zeros.py` |
| `06-decidir-e-repetir` | `rateio_simples.py`, `se_v0.py`, `portes.py`, `cota_comercio.py`, `metade.py` |
| `07-funcoes-que-a-marlene-nao-escreveu` | `compara_abas.py`, `funcoes.py`, `funcoes_v0.py`, `fator_funcao.py`, `br.py`, `duplicados.py` |
| `08-quando-da-errado-de-proposito` | `consumo_v0.py`, `validacao.py`, `valida.py`, `numero_br_funcao.py`, `valida_ano.py` |
| `09-arquivos-encodings-e-o-joao-que-virou-joao` | `encoding.py`, `abadiania_v0.py`, `leituras_c.py`, `qual_encoding.py` |
| `10-objetos-que-representam-coisas` | `modelos.py`, `testa_modelos.py`, `usina.py`, `mesmo_cooperado.py` |
| `11-um-arquivo-vira-um-pacote` | `funcoes.py`, `rateio/__init__.py`, `rateio/cpf.py`, `rateio/calculo.py`, `rateio/modelos.py`, `rateio/cadastro.py`, `rateio/__main__.py`, `confere_ambiente.py` |
| `12-catorze-milhoes-de-leituras` | `leitura_ano.py`, `compara.py`, `por_usina.py`, `metade_energia.py` |
| `13-fatiar-filtrar-transmitir` | `diario.py`, `lacunas.py`, `estima_lacunas.py`, `melhor_fator.py` |
| `14-vetores-e-matrizes-agora-rapidos` | `similaridade.py`, `inversores.py`, `sorteio.py`, `sorteio_usinas.py`, `sem_fevereiro.py` |
| `15-uma-tabela-com-nome-nas-colunas` | `le_inversores.py`, `estacao.py`, `corumba_ano.py` |
| `16-selecionar-sem-procv` | `refaz_planilha.py`, `cotas_por_usina.py`, `aba_visivel.py` |
| `17-o-cpf-com-e-sem-ponto` | `limpa_cadastro.py`, `causa1.py`, `pares.py`, `consumo_tipos.py` |
| `18-wh-kwh-e-a-virgula` | `rateio/leitura.py`, `faixa.py`, `foto.py`, `rateio/limpeza.py`, `causa2.py`, `faixa_ano.py` |
| `19-agrupar-e-a-tabela-dinamica-que-da-para-reler` | `rateio/geracao.py`, `tabela_assembleia.py`, `credito_por_tipo.py`, `dias_fracos.py` |
| `20-juntar-sem-perder-ninguem` | `cruzamento.py`, `confere_juncao.py`, `como_devia.py` |
| `21-o-dia-que-comeca-as-21h` | `rateio/fuso.py`, `causa3.py`, `perfil_hora.py`, `fuso_c.py` |
| `22-graficos-para-a-assembleia` | `graficos.py`, `titulos_v0.py`, `cocalzinho_ano.py`, `faixas.py` |
| `23-o-notebook-que-da-um-numero-diferente-toda-vez` | `monta_notebook.py`, `le_notebook.py`, `roda_celulas.py`, `sementes.py`, `quem_leva.py`, `credito_dirceu.py`, `perda.py`, `do_zero.py` |
| `24-de-onde-veio-esse-numero` | `rateio/manifesto.py`, `manifesto_brutos.py`, `confere_brutos.py`, `copia_do_wesley.py`, `confere_copia.py`, `compara_copia.py`, `rateio/dicionario.py`, `confere_colunas.py`, `fevereiro_corrigido.py`, `confere_copia2.py`, `confere_origem.py` |
| `25-git-para-quem-salvava-v7_agora_vai` | `.gitignore`, `rateio/calculo.py`, `rateio/__init__.py` |
| `26-testes-que-a-dra-ana-clara-aceita` | `tests/test_calculo.py`, `tests/test_limpeza.py`, `tests/test_fuso.py`, `tests/test_cpf.py`, `tests/test_fevereiro.py`, `tests/test_cota_zero.py`, `tests/test_cadastro.py`, `tests/test_dias.py` |
| `27-quarenta-minutos-para-cruzar-duas-listas` | `cruza.py`, `cresce.py`, `consumo_anual.py`, `binaria.py` |
| `28-memoria-tambem-acaba` | `marco_texto.py`, `rateio/leituras.py`, `marco_tipos.py`, `pedacos.py`, `parquet.py`, `ano_parquet.py` |
| `29-duas-regras-de-rateio` | `rateio/registro.py`, `experimento.py`, `cenarios.py`, `por_tipo.py`, `limite.py` |
| `30-o-pipeline-roda-sozinho` | `rateio.toml`, `rateio/pipeline.py`, `rateio/__main__.py`, `rateio/__init__.py`, `estraga_manifesto.py`, `rateio_teste.toml`, `rodar.sh` |
| `31-sabado-24-de-abril` | `rateio/reconciliacao.py`, `vinte_centavos.py`, `tests/test_reconciliacao.py`, `README.md`, `sede_no_ano.py`, `tests/test_sede.py` |
| `a3-o-gerador-da-coopersol` | `confere_dados.py`, `dados/mundo.py`, `dados/ceu.py`, `dados/inversores.py`, `dados/cadastro.py`, `dados/ged.py`, `dados/planilha.py`, `dados/gerar_coopersol.py` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
