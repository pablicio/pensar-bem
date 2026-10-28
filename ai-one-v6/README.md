# Materiais — AI One — Volume 6: Sequências e Memória

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t ai-one-v6 .
docker run --rm -it -v "${PWD}:/projeto" ai-one-v6 bash
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
docker run --rm -it -p 8888:8888 -v "${PWD}:/projeto" ai-one-v6 jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `requirements.txt`
- `projeto/ (6 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `ola.py`, `requirements.txt`, `Dockerfile`, `versoes.py`, `abre_serie.py` |
| `01-tres-mil-e-quatrocentas-pessoas-no-ginasio` | `regra_antiga.py`, `serie.py` |
| `02-o-rio-amanha-e-o-rio-hoje` | `rio/__init__.py`, `rio/avalia.py`, `persistencia.py`, `picos.py`, `autocorrelacao.py` |
| `03-quarenta-anos-num-caderno` | `lacunas.py`, `rio/serie.py`, `digitacao.py`, `degrau.py`, `interpola.py`, `limpa.py` |
| `04-janelas` | `rio/janelas.py`, `rio/avalia.py`, `boosting.py`, `mlp.py`, `tamanho.py` |
| `05-um-estado-que-passa-adiante` | `reservatorio.py`, `rio/numpy_rnn.py`, `rnn_chuva.py`, `impulso.py` |
| `06-derivar-no-tempo` | `rio/numpy_rnn.py`, `bptt.py`, `culpa.py`, `treina_numpy.py` |
| `07-a-memoria-que-some` | `jacobiana.py`, `rio/numpy_treino.py`, `recorte.py`, `memoria.py` |
| `08-uma-dissertacao-de-1991` | `elman.py` |
| `09-uma-esteira-com-portas` | `rio/numpy_lstm.py`, `confere_lstm.py`, `soma_lstm.py` |
| `10-a-mesma-ideia-com-menos-pecas` | `rio/numpy_gru.py`, `confere_gru.py`, `compara.py` |
| `11-as-mesmas-redes-em-pytorch` | `formatos.py`, `copia.py`, `velocidade.py`, `tempo.py` |
| `12-chuva-la-em-cima-agua-aqui-embaixo` | `rio/entradas.py`, `correlacao.py`, `rio/janelas.py`, `boosting_tudo.py` |
| `13-uma-lstm-para-o-nivel-do-rio` | `rio/entradas.py`, `rio/modelos.py`, `rio/treino.py`, `lstm_rio.py`, `evento.py` |
| `14-doze-horas-a-frente` | `rio/modelos.py`, `direta.py`, `enc_dec.py`, `rio/recursiva.py`, `recursiva.py`, `horizonte.py` |
| `15-o-pico-que-a-media-esconde` | `rio/cota.py`, `rio/treino.py`, `pesos.py`, `cotas.py` |
| `16-quanto-confiar-na-previsao` | `rio/quantis.py`, `quantis.py`, `faixa.py` |
| `17-dois-mil-e-oito` | `rio/reserva.py`, `faixa_treino.py`, `reserva.py` |
| `18-o-alarme-que-o-major-aceita` | `rio/alerta.py`, `politica.py`, `simulacao.py` |
| `19-mil-e-duzentas-mensagens-numa-noite` | `rio/texto.py`, `noite.py`, `vocabulario.py` |
| `20-palavras-viram-vetores` | `rio/vetores.py`, `vetores.py`, `vizinhos.py` |
| `21-uma-rede-que-le-da-esquerda-para-a-direita` | `rio/leitor.py`, `leitor.py`, `rio/provinha.py`, `prova.py`, `fila.py`, `sementes.py` |
| `22-e-da-direita-para-a-esquerda` | `rio/bayes.py`, `compara.py` |
| `23-o-boato-da-barragem` | `boatos.py`, `rio/triagem.py`, `erros.py`, `limiar.py` |
| `24-sequencia-para-sequencia` | `rio/extrator.py`, `extrator.py`, `avalia_extrator.py` |
| `25-convolucoes-no-tempo` | `rio/convolucao.py`, `conv_rio.py`, `todas_as_horas.py` |
| `26-o-modelo-de-plantao` | `rio/plantao.py`, `treina_plantao.py`, `ensaio.py`, `plantao_hora.py` |
| `27-a-estacao-que-parou-de-mandar` | `rio/estacoes.py`, `treina_reservas.py`, `falha_nas_cheias.py`, `rio/plantao.py`, `ensaio_reserva.py`, `travado.py` |
| `28-o-simulado` | `simulado.py`, `resumo_simulado.py`, `histerese.py` |
| `29-prestacao-de-contas` | `relatorio.py` |
| `30-outubro` | `rio/espera.py`, `outubro.py` |
| `31-o-que-a-rede-esquece` | `tempos.py`, `rio/atencao.py`, `atencao.py`, `compara_atencao.py` |
| `a3-o-gerador-do-rio` | `confere_dados.py`, `dados/chuva.py`, `dados/bacia.py`, `dados/gerar_rio.py`, `dados/frases.py`, `dados/gerar_mensagens.py` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
