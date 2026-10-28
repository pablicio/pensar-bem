# Materiais — AI One — Volume 5: Visão Computacional

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t ai-one-v5 .
docker run --rm -it -v "${PWD}:/projeto" ai-one-v5 bash
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
docker run --rm -it -p 8888:8888 -v "${PWD}:/projeto" ai-one-v5 jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `requirements.txt`
- `projeto/ (5 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `ola.py`, `requirements.txt`, `Dockerfile`, `versoes.py`, `dados/baixar_mnist.py`, `dados/baixar_pesos.py`, `abre_folha.py`, `classes.py` |
| `01-ferrugem-ou-sol` | `foto.py`, `recorte.py`, `cores.py` |
| `02-uma-imagem-e-uma-matriz-que-alguem-fotografou` | `tamanho.py`, `folha/__init__.py`, `folha/conjunto.py`, `divide.py`, `vazamento.py`, `media.py` |
| `03-o-mlp-que-contava-pixels` | `folha/treino.py`, `mlp.py`, `desloca.py` |
| `04-um-filtro-de-tres-por-tres` | `folha/convolucao.py`, `passo_a_passo.py`, `convolucao.py` |
| `05-passo-preenchimento-e-canais` | `folha/convolucao.py`, `canais.py`, `formatos.py`, `um_por_um.py` |
| `06-a-convolucao-e-um-produto-de-matrizes` | `folha/convolucao.py`, `pequeno.py`, `faixas.py`, `corrida.py` |
| `07-o-filtro-que-se-aprende` | `folha/convolucao.py`, `gradiente.py`, `treina_cnn.py`, `filtros.py` |
| `08-resumir-sem-perder-o-essencial` | `pooling.py`, `equivariancia.py`, `folha/redes.py`, `campo.py`, `desloca_cnn.py` |
| `09-uma-rede-de-1998` | `folha/redes.py`, `mnist.py`, `lenet_mnist.py`, `lenet_folhas.py` |
| `10-setembro-de-2012` | `folha/custo.py`, `arquiteturas.py` |
| `11-blocos-de-tres-por-tres` | `tres_por_tres.py`, `folha/redes.py`, `tempo_vgg.py`, `profundidade.py` |
| `12-muitos-caminhos-de-uma-vez` | `folha/redes.py`, `custo_inception.py`, `inception_folhas.py` |
| `13-atalhos-que-deixam-aprender` | `folha/redes.py`, `residual.py`, `gradiente.py` |
| `14-normalizar-canais` | `por_canal.py`, `folha/resnet.py`, `treina_bn.py`, `lote.py`, `reestima.py`, `funde.py` |
| `15-folhas-giradas` | `giradas.py`, `folha/giradas.py`, `aumenta.py`, `quinas.py`, `cores.py`, `recorte.py`, `previsao.py`, `mostra.py` |
| `16-pesos-emprestados-da-imagenet` | `folha/emprestada.py`, `primeira_camada.py`, `extrai.py`, `compara.py`, `poucas.py`, `mapa.py` |
| `17-descongelar-com-cuidado` | `folha/ajuste.py`, `descongela.py` |
| `18-o-agronomo-discorda-do-agronomo` | `concordancia.py`, `teto.py`, `ruido.py`, `suspeitas.py` |
| `19-a-rede-aprendeu-a-mesa` | `folha/fundos.py`, `treina.py`, `contrafactual.py`, `folha/olhar.py`, `mapas.py`, `onde_olha.py` |
| `20-metricas-por-doenca` | `confusao.py`, `decisao.py` |
| `21-uma-caixa-em-volta-da-lesao` | `folha/caixas.py`, `iou.py`, `folha/localizacao.py`, `localiza.py`, `desenha_caixas.py` |
| `22-a-ponta-e-o-peciolo` | `folha/pontos.py`, `pontos.py`, `endireita.py` |
| `23-muitas-caixas-uma-resposta` | `folha/deteccao.py`, `janelas.py`, `nms_folha.py`, `ap.py` |
| `24-uma-olhada-so` | `folha/yolo.py`, `ancoras.py`, `treina_yolo.py`, `avalia_yolo.py`, `desenha_yolo.py`, `tempo_yolo.py` |
| `25-duas-etapas` | `folha/duas_etapas.py`, `ajusta_faster.py`, `propostas.py`, `compara.py`, `tempos.py` |
| `26-subir-a-resolucao` | `folha/transposta.py`, `transposta.py`, `tabuleiro.py` |
| `27-pixel-a-pixel` | `folha/unet.py`, `segmenta.py`, `desenha_mascaras.py` |
| `28-quanto-da-folha-esta-doente` | `severidade.py`, `conta_lesoes.py` |
| `29-fotos-do-mundo-real` | `folha/qualidade.py`, `mundo_real.py` |
| `30-caber-no-bolso` | `separavel.py`, `folha/bolso.py`, `compara_bolso.py`, `exporta.py`, `tempo_onnx.py` |
| `31-a-folha-parecida` | `folha/siamesa.py`, `treina_siamesa.py`, `vizinhas.py`, `aureolada.py`, `poucas_fotos.py` |
| `32-antes-do-agronomo-nunca-no-lugar-dele` | `folha/decisao.py`, `calibra.py`, `encaminha.py` |
| `33-o-conjunto-de-dados-e-o-produto` | `cartao.py`, `ativo.py` |
| `34-a-visita-de-campo` | `campo.py` |
| `35-quinze-de-setembro` | `dia_15.py` |
| `36-o-que-a-rede-ve` | `sonhos.py`, `estilo.py`, `embaralha.py` |
| `a1-formatos-e-formulas` | `confere_formulas.py` |
| `a2-arquiteturas-de-bolso` | `fichas.py` |
| `a3-o-gerador-das-folhas` | `confere_folhas.py`, `dados/desenho.py`, `dados/camera.py`, `dados/gerar_conjunto.py` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
