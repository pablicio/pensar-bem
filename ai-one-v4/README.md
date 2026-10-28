# Materiais — AI One — Volume 4: Redes Neurais

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t ai-one-v4 .
docker run --rm -it -v "${PWD}:/projeto" ai-one-v4 bash
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
docker run --rm -it -p 8888:8888 -v "${PWD}:/projeto" ai-one-v4 jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `requirements.txt`
- `projeto/ (4 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `ola.py`, `requirements.txt`, `Dockerfile`, `versoes.py`, `dados/baixar_mnist.py`, `mnist.py`, `desenha.py` |
| `01-dois-virgula-tres-por-cento` | `mostra_digito.py`, `medias.py`, `centroide.py` |
| `02-uma-ideia-de-1943` | `neuronio_1943.py` |
| `03-o-perceptron-decide` | `perceptron.py`, `desenha_pesos.py`, `tres_e_oito.py` |
| `04-o-xor-que-parou-a-pesquisa` | `xor_perceptron.py`, `xor_a_mao.py`, `xor_espacos.py` |
| `05-funcoes-que-dobram-o-espaco` | `tres_lineares.py`, `ativacoes.py`, `xor_relu.py` |
| `06-quanto-o-modelo-errou` | `softmax_ingenua.py`, `perdas.py`, `estavel.py`, `compara_perdas.py` |
| `07-uma-conta-vira-um-grafo` | `grafo.py` |
| `08-backpropagation-a-mao` | `backprop_a_mao.py` |
| `09-um-motor-de-derivadas-em-oitenta-linhas` | `motor/__init__.py`, `motor/valor.py`, `motor/rede.py`, `pontos.py`, `treina_pontos.py` |
| `10-de-escalares-para-matrizes` | `numpy_mlp/__init__.py`, `numpy_mlp/camadas.py`, `confere_matricial.py`, `tempo.py` |
| `11-descer-a-ladeira-com-pressa` | `numpy_mlp/dados.py`, `numpy_mlp/otimizadores.py`, `numpy_mlp/treino.py`, `mlp.py`, `tamanho_do_lote.py` |
| `12-momento-e-adam` | `numpy_mlp/otimizadores.py`, `vale.py`, `compara_otimizadores.py` |
| `13-o-passo-certo` | `passo_grande.py`, `faixa_de_taxa.py`, `agenda.py`, `taxa_pequena.py` |
| `14-comecar-do-jeito-certo` | `pesos_iguais.py`, `numpy_mlp/camadas.py`, `sinal_profundo.py`, `dez_camadas.py` |
| `15-normalizar-no-meio-do-caminho` | `numpy_mlp/camadas.py`, `confere_norm.py`, `com_e_sem.py`, `esqueceu.py` |
| `16-decorar-nao-e-aprender` | `numpy_mlp/camadas.py`, `numpy_mlp/otimizadores.py`, `numpy_mlp/aumento.py`, `numpy_mlp/treino.py`, `regulariza.py` |
| `17-tensores-e-o-mesmo-motor-industrial` | `tensores.py`, `mesmo_grafo.py`, `precisao.py` |
| `18-a-rede-vira-um-modulo` | `leitora/__init__.py`, `leitora/modelo.py`, `treina_torch.py` |
| `19-dados-que-chegam-em-lotes` | `leitora/recorte.py`, `leitora/dados.py`, `lotes.py`, `trabalhadores.py` |
| `20-o-laco-de-treino-que-a-joana-copiou` | `leitora/modelo.py`, `copiado.py`, `leitora/treino.py`, `reprodutivel.py`, `retoma.py` |
| `21-onde-a-rede-erra` | `leitora/carrega.py`, `treina_leitora.py`, `onde_erra.py`, `galeria.py` |
| `22-a-rede-tem-certeza-demais` | `leitora/calibra.py`, `confiabilidade.py`, `calibracao.py` |
| `23-quando-nao-ler` | `leitora/decide.py`, `cobertura.py`, `custo.py` |
| `24-digitos-da-casa` | `ajuste_fino.py`, `de_novo.py`, `leitora/decide.py` |
| `25-tres-digitos-numa-caixa` | `leitora/resposta.py`, `le_cartoes.py` |
| `26-a-rede-contra-a-arvore` | `gera_abstencao.py`, `rede_contra_arvore.py` |
| `27-auditavel` | `leitora/auditoria.py`, `audita.py`, `contestacao.py` |
| `28-a-noite-de-leitura` | `dados/inverno.py`, `leitora/noite.py`, `vazao.py`, `noite.py` |
| `29-trinta-de-julho` | `sabado.py`, `embaralha.py` |
| `a1-as-derivadas-do-livro` | `confere_derivadas.py` |
| `a2-pytorch-de-bolso` | `equivalencias.py` |
| `a3-o-gerador-dos-cartoes` | `confere_cartoes.py`, `dados/tracos.py`, `dados/desenho.py`, `dados/formulario.py`, `dados/gerar_formularios.py` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
