# Materiais — AI One — Volume 8: Atenção e Transformers

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t ai-one-v8 .
docker run --rm -it -v "${PWD}:/projeto" ai-one-v8 bash
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
docker run --rm -it -p 8888:8888 -v "${PWD}:/projeto" ai-one-v8 jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `requirements.txt`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `ola.py`, `requirements.txt`, `Dockerfile`, `versoes.py`, `lupa/__init__.py`, `lupa/diario.py`, `abre_diarios.py` |
| `01-requalificacao-viaria` | `lupa/busca.py`, `busca.py`, `depois.py`, `perplexidade.py` |
| `02-o-gargalo` | `lupa/extrator.py`, `gargalo.py`, `influencia.py` |
| `03-olhar-para-tras-com-pesos` | `lupa/alinhamento.py`, `atencao_rnn.py`, `atalho.py`, `mapa.py` |
| `04-consulta-chave-e-valor` | `lupa/atencao_numpy.py`, `atencao.py`, `lupa/qkv_rnn.py`, `qkv_rnn.py` |
| `05-a-derivada-da-atencao` | `jacobiana.py`, `lupa/atencao_numpy.py`, `derivadas.py`, `saturacao.py` |
| `06-por-que-dividir-pela-raiz-de-d` | `variancia.py`, `entropia.py`, `sem_escala.py` |
| `07-cada-palavra-olha-para-todas` | `media_passado.py`, `lupa/atencao_numpy.py`, `equivariancia.py`, `custo.py`, `lupa/autoatencao.py`, `autoatencao_torch.py` |
| `08-varias-cabecas` | `lupa/cabecas.py`, `formatos.py`, `leitor.py` |
| `09-onde-fica-cada-palavra` | `lupa/posicao.py`, `ondas.py`, `rope.py`, `deslocamento.py` |
| `10-junho-de-2017` | `contagem.py` |
| `11-um-bloco-de-cada-vez` | `layernorm.py`, `gelu.py`, `lupa/bloco.py`, `um_bloco.py`, `pre_pos.py` |
| `12-codificador-decodificador-ou-os-dois` | `lupa/tradutor.py`, `datas.py`, `so_decodificador.py` |
| `13-o-que-e-um-token` | `utf8.py`, `unidades.py` |
| `14-pares-que-se-fundem` | `lupa/bpe.py`, `fusoes.py`, `curva_bpe.py` |
| `15-pontos-virgulas-e-o-c-decomposto` | `renan.py`, `formas.py`, `lupa/tokenizador.py`, `tokeniza.py`, `biblioteca.py` |
| `16-um-modelo-de-linguagem-de-bigramas` | `lupa/corpus.py`, `bigramas.py`, `rede_bigramas.py` |
| `17-um-gpt-pequeno` | `lupa/gpt.py`, `adamw.py`, `gpt_pequeno.py`, `escreve.py` |
| `18-temperatura-top-k-e-top-p` | `temperatura.py`, `lupa/escolha.py`, `estrategias.py`, `feixe.py` |
| `19-o-cnpj-que-nao-existe` | `lupa/cnpj.py`, `verificador.py`, `cnpjs.py`, `digitos.py`, `calibracao.py` |
| `20-escala` | `flops.py`, `escala.py`, `chinchilla.py` |
| `21-esconder-palavras-para-aprender` | `lupa/mlm.py`, `lupa/bert.py`, `treina_bert.py`, `adivinha.py`, `bert_hf.py` |
| `22-ajuste-fino-para-licitacoes` | `lupa/ajuste.py`, `ajuste.py`, `intervalo.py` |
| `23-objeto-valor-prazo` | `regras.py`, `lupa/etiquetas.py`, `entidades.py` |
| `24-busca-por-significado` | `lupa/vetores.py`, `contraste.py`, `busca_vetores.py` |
| `25-pre-treinar-ajustar-instruir` | `lupa/instrucao.py`, `instrui.py`, `kl_otimo.py`, `preferencias.py` |
| `26-contexto-longo-conta-longa` | `lupa/kv.py`, `cache.py`, `lupa/flash.py`, `flash_teste.py` |
| `27-imagens-em-pedacos` | `lupa/escaneado.py`, `pedacos.py`, `lupa/vit.py`, `visao.py` |
| `28-o-pipeline-das-sete` | `lupa/alerta.py`, `sete.py` |
| `29-avaliar-o-que-o-cliente-nao-viu` | `avaliacao.py` |
| `30-trinta-e-um-de-maio` | `renovacao.py` |
| `31-atencao-e-quase-tudo` | `inventario.py` |
| `a1-o-transformer-numa-pagina` | `uma_pagina.py` |
| `a2-as-derivadas-do-transformer` | `derivadas_a2.py` |
| `a3-o-gerador-dos-diarios` | `dados/__init__.py`, `dados/extenso.py`, `dados/nomes.py`, `dados/objetos.py`, `dados/atos.py`, `dados/gerar_corpus.py` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
