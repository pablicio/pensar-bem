# Materiais — AI One — Volume 3: Machine Learning

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t ai-one-v3 .
docker run --rm -it -v "${PWD}:/projeto" ai-one-v3 bash
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
docker run --rm -it -p 8888:8888 -v "${PWD}:/projeto" ai-one-v3 jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `requirements.txt`
- `projeto/ (6 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `ola.py`, `requirements.txt`, `Dockerfile`, `versoes.py` |
| `01-sete-virgula-sete-por-cento` | `regra_jussara.py`, `regra_2024.py`, `por_regra.py`, `por_agente.py` |
| `02-antes-do-modelo-a-pergunta` | `risco/__init__.py`, `risco/alvo.py`, `alvo_tabela.py`, `safras.py` |
| `04-o-modelo-que-chuta-a-media` | `visitas.py`, `modelo_do_icaro.py`, `treino_teste.py`, `mediana.py`, `sementes.py` |
| `05-quanto-a-costureira-fatura` | `uma_reta.py`, `varias_colunas.py`, `dona_cida.py` |
| `06-colunas-que-nao-sao-numeros` | `visitas.py`, `pipeline_faturamento.py`, `cliente_novo.py`, `sem_um_grupo.py`, `ordinal.py` |
| `07-retas-demais` | `polinomios.py`, `curva_validacao.py`, `trezentos.py`, `variancia.py`, `mais_dados.py` |
| `08-freio-no-coeficiente` | `ridge_a_mao.py`, `freio.py`, `caminhos.py`, `variancia_ridge.py`, `sobreviventes.py` |
| `09-sim-ou-nao-com-probabilidade` | `risco/dados.py`, `logistica_a_mao.py`, `primeiro_modelo.py`, `dona_cida_risco.py`, `perda_validacao.py`, `mais_colunas.py` |
| `10-noventa-por-cento-aprovando-todo-mundo` | `risco/modelos.py`, `aprova_todo_mundo.py`, `precisao_revocacao.py`, `cortes.py` |
| `11-onde-cortar` | `risco/lucro.py`, `curva_lucro.py`, `roc.py`, `margem.py`, `inadimplencia_corte.py` |
| `12-a-probabilidade-que-mente` | `confiabilidade.py`, `calibra.py`, `auc_calibrada.py` |
| `13-um-teste-so-e-sorte` | `sementes.py`, `validacao_cruzada.py`, `no_tempo.py`, `por_cliente.py`, `lado_a_lado.py` |
| `14-a-variavel-que-sabia-o-futuro` | `vaza.py`, `noventa_e_nove.py`, `caca.py`, `ruido.py`, `saldo.py`, `producao.py` |
| `15-os-vizinhos-da-dona-cida` | `vizinhos_cida.py`, `escolhe_k.py`, `maldicao.py`, `distancias.py` |
| `16-probabilidade-ingenua` | `finalidades.py`, `bayes_a_mao.py`, `frases_novas.py`, `finalidade_risco.py`, `palavras_fortes.py`, `com_finalidade.py` |
| `17-a-margem-mais-larga` | `margem.py`, `idade_risco.py`, `fronteiras.py`, `desenha_fronteiras.py`, `valor_de_c.py` |
| `18-perguntas-em-sequencia` | `gini.py`, `arvore_rasa.py`, `arvore_contra_regra.py`, `profundidade.py`, `folha_minima.py` |
| `19-uma-floresta-que-discorda` | `arvores_da_cida.py`, `floresta.py`, `importancias.py`, `quantas_arvores.py` |
| `20-arvores-que-corrigem-as-anteriores` | `boosting_a_mao.py`, `risco/modelos.py`, `boosting.py`, `taxa.py`, `com_finalidade.py` |
| `21-ajustar-botoes-sem-trapacear` | `botoes.py`, `risco/finalidade.py`, `risco/dados.py`, `a_busca_do_icaro.py`, `busca_honesta.py`, `grade.py` |
| `22-clientes-que-se-parecem` | `atrasos.py`, `kmeans_a_mao.py`, `quantos_grupos.py`, `perfis.py`, `sem_escala.py` |
| `23-vinte-e-tres-colunas-em-duas` | `larga.py`, `pca_a_mao.py`, `componentes.py`, `mapa.py`, `quantos_componentes.py` |
| `24-a-conta-que-nao-se-parece-com-nenhuma` | `recentes.py`, `isolamento.py`, `com_telefone.py`, `distancia.py`, `sem_telefone.py` |
| `25-por-que-o-modelo-recusou-a-dona-cida` | `pedido_da_cida.py`, `por_que_recusou.py`, `risco/campeao.py`, `importancia_global.py`, `dependencia.py`, `risco/explica.py`, `e_se.py`, `o_que_mudaria.py`, `golpe_e_se.py` |
| `26-justo-para-quem` | `regioes.py`, `por_regiao.py`, `prefixo.py`, `com_prefixo.py`, `um_corte_por_regiao.py` |
| `27-pouco-inadimplente-muito-problema` | `precoce.py`, `ignora.py`, `remedios.py`, `limiar.py`, `corrige.py` |
| `28-o-modelo-vira-um-arquivo` | `inspeciona.py`, `o_que_o_pickle_importa.py`, `salva.py`, `carrega.py`, `cartao.py` |
| `29-o-mundo-muda-depois-do-deploy` | `risco/monitor.py`, `em_producao.py`, `psi_semanal.py`, `psi_por_coluna.py`, `o_que_se_sabe.py`, `psi_do_acaso.py` |
| `30-a-reuniao-com-o-atlantico-sul` | `politicas.py`, `fora_do_tempo.py`, `por_mes.py`, `intervalo.py`, `por_produto.py` |
| `31-trinta-de-junho` | `concedidos.py`, `fechamento.py`, `safras.py`, `sem_recusar.py`, `golpe_no_covenant.py` |
| `a3-o-gerador-da-carteira` | `confere_dados.py`, `dados/mundo.py`, `dados/textos.py`, `dados/carteira.py`, `dados/cobranca.py`, `dados/gerar_carteira.py`, `dados/gerar_producao.py` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
