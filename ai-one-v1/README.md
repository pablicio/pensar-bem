# Materiais — AI One — Volume 1: Matemática para IA

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t ai-one-v1 .
docker run --rm -it -v "${PWD}:/projeto" ai-one-v1 bash
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
docker run --rm -it -p 8888:8888 -v "${PWD}:/projeto" ai-one-v1 jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `ola.py`, `Dockerfile` |
| `02-a-calculadora-que-obedece` | `pedido.py`, `pedido2.py`, `diferenca.py` |
| `03-receitas-com-nome` | `frete.py`, `tabela_frete.py`, `grafico_frete.py`, `grafico_degraus.py`, `tabela_compactos.py`, `tres_quilos.py`, `frete_por_disco.py` |
| `04-a-reta-do-preco` | `reta.py`, `tabela_reta.py`, `etiquetas.py`, `repasse.py`, `dois_pontos.py` |
| `05-o-disco-que-dobra-de-preco` | `valorizacao.py`, `dobra.py`, `numero_e.py`, `reedicao.py`, `paebiru.py`, `reedicao2.py`, `soma_infinita.py` |
| `06-decibeis-oitavas-e-outros-logaritmos` | `escala_log.py`, `meses_exatos.py` |
| `07-funcoes-que-dizem-sim-ou-nao` | `sigmoide.py`, `curvas.py`, `simetria.py`, `logit.py` |
| `08-um-disco-tem-seis-numeros` | `catalogo.csv`, `catalogo.py`, `vetores.py`, `operacoes.py`, `lista_beto.py`, `setas.py`, `baile_piano.py`, `lista_domingo.py`, `diferenca_discos.py` |
| `09-quanto-um-disco-parece-com-outro` | `distancias.py`, `catalogo.csv`, `vizinhos.py`, `culpado.py`, `normaliza.py`, `vizinhos_normalizados.py`, `confere_distancia.py`, `vizinhos_manhattan.py`, `ponderada.py` |
| `10-o-angulo-entre-dois-gostos` | `clientes.csv`, `clientes.py`, `similaridade.py`, `parecidos_lindalva.py`, `angulos.py`, `unitarios.py` |
| `11-a-tabela-que-e-uma-matriz` | `matriz.py`, `reedicao_email.py`, `totais.py`, `tamanho_loja.py`, `reedicao_jazz.py`, `proporcoes.py` |
| `12-multiplicar-matrizes-e-encadear-transformacoes` | `matriz.py`, `casinha.py`, `transforma.py`, `rotacao.py` |
| `13-tres-dimensoes-latentes` | `notas.csv`, `fatores.py`, `parametros.py`, `so_media.py` |
| `14-as-direcoes-que-nao-giram` | `potencia.py`, `nuvem.csv`, `direcao_gosto.py`, `passo_a_passo.py`, `segunda_direcao.py` |
| `15-quanto-muda-quando-muda-um-pouco` | `demanda.py`, `derivada_numerica.py`, `tangente.py`, `derivada_exponencial.py` |
| `16-regras-para-nao-calcular-limite-toda-vez` | `regras.py`, `derivada_sigmoide.py` |
| `17-o-preco-que-maximiza-a-receita` | `lucro.py`, `melhor_preco.py`, `custo_45.py`, `com_limite.py` |
| `18-varias-alavancas-ao-mesmo-tempo` | `duas_alavancas.py`, `mapa.py`, `busca_topo.py` |
| `19-descendo-a-ladeira-no-escuro` | `descida.py`, `descida_loja.py`, `eta_meio.py`, `eta_quatro.py`, `limite_eta.py` |
| `20-somar-muitos-pedacinhos` | `promocao.py`, `integral.py`, `retangulos.py`, `quinze_minutos.py` |
| `21-cara-ou-coroa-na-vitrine` | `simula.py`, `frequencia.py`, `os_tres.py`, `mil_sabados.py`, `amigos.py` |
| `22-quem-comprou-alceu-tambem-comprou` | `bayes.py`, `meio_a_meio.py` |
| `23-media-mediana-e-o-disco-de-nove-mil-reais` | `gerar_balcao.py`, `resumo.py`, `dezembro.py`, `padroniza.py` |
| `24-o-formato-do-acaso` | `distribuicoes.py`, `sextas.py`, `dias.py`, `com_anuncio.py`, `um_desvio.py` |
| `25-quanto-vale-um-lote-de-quatro-mil-discos` | `acervo.py`, `amostra.py`, `confere_faixa.py`, `tamanhos.py`, `sem_estante.py` |
| `26-surpresa-se-mede-em-bits` | `informacao.py`, `curva.py`, `previsoes.py`, `compara.py`, `chute.py`, `calibra.py` |
| `27-o-asteroide-que-sumiu-atras-do-sol` | `vendidos.py`, `minimos.py`, `ajuste.py`, `medias.py`, `centraliza.py` |
| `28-um-recomendador-de-bolso` | `loja.py`, `recomenda.py`, `cliente.py`, `avalia.py`, `em_n.py` |
| `29-fatorando-o-gosto` | `fatoracao.py`, `treina.py`, `mapa.py`, `regulariza.py` |
| `30-o-slide-27` | `slide27.py`, `tres_versoes.py`, `jazzista.py` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
