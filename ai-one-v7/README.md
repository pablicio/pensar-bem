# Materiais — AI One — Volume 7: Autoencoders e GANs

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t ai-one-v7 .
docker run --rm -it -v "${PWD}:/projeto" ai-one-v7 bash
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
docker run --rm -it -p 8888:8888 -v "${PWD}:/projeto" ai-one-v7 jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `requirements.txt`
- `projeto/ (5 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `ola.py`, `requirements.txt`, `Dockerfile`, `versoes.py`, `abre_acervo.py` |
| `01-catorze-mil-estampas-e-um-pedido` | `lauber/__init__.py`, `lauber/acervo.py`, `lauber/classificador.py`, `classifica.py`, `desenha_floral.py` |
| `02-comprimir-e-entender` | `lauber/pca.py`, `comprime_pca.py` |
| `03-uma-rede-que-copia-a-si-mesma` | `lauber/autoencoder.py`, `denso.py` |
| `04-convolucoes-que-desfazem-convolucoes` | `lauber/convolucional.py`, `convolucional.py` |
| `05-o-mapa-das-estampas` | `mapa.py` |
| `06-um-furo-em-cada-dez-mil-metros` | `lauber/anomalia.py`, `detecta.py` |
| `07-onde-esta-o-defeito` | `localiza.py` |
| `08-o-tear-que-muda-de-fio` | `semana.py` |
| `09-na-linha-de-producao` | `vazao.py`, `conta.py` |
| `10-restaurar-sem-inventar` | `lauber/restaura.py`, `restaura.py` |
| `11-um-ponto-vira-uma-nuvem` | `nuvens.py` |
| `12-o-truque-da-reparametrizacao` | `lauber/vae.py`, `sem_kl.py` |
| `13-reconstruir-e-organizar` | `vae_mapa.py` |
| `14-o-peso-do-kl` | `beta.py` |
| `15-andar-no-espaco-latente` | `anda.py`, `lauber/condicional.py`, `condicional.py` |
| `16-uma-noite-em-montreal` | `gan1d.py` |
| `17-o-falsificador-e-o-perito` | `lauber/gan.py`, `perdas.py` |
| `18-sempre-a-mesma-estampa` | `colapso.py` |
| `19-as-regras-da-dcgan` | `densa.py`, `lauber/dcgan.py`, `dcgan.py` |
| `20-equilibrio-que-nao-converge` | `lauber/wgan.py`, `fim_de_semana.py`, `wgan_gp.py` |
| `21-estampa-por-encomenda` | `lauber/encomenda.py`, `encomenda.py` |
| `22-como-medir-uma-estampa-que-nao-existe` | `lauber/medidas.py`, `medidas.py`, `as_cegas.py` |
| `23-essa-estampa-ja-existe` | `lauber/vizinhos.py`, `synapsys.py`, `copia.py` |
| `24-autoencoder-vae-ou-gan` | `compara.py` |
| `25-a-estampa-que-emenda` | `lauber/emenda.py`, `costura.py`, `emenda.py` |
| `26-seis-cores-na-mesa-de-serigrafia` | `lauber/serigrafia.py`, `cores.py` |
| `27-a-assinatura-da-zuleica` | `lauber/procedencia.py`, `registro.py` |
| `28-o-showroom` | `lauber/vitrine.py`, `juntas.py`, `funil.py` |
| `29-dez-de-agosto` | `na_hora.py` |
| `30-o-que-ainda-falta` | `lauber/resolucao.py`, `resolucao.py` |
| `a3-o-gerador-do-acervo` | `confere_dados.py`, `dados/estampas.py`, `dados/gerar_acervo.py`, `dados/gerar_malha.py` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
