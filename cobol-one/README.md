# Materiais — COBOL One: Mainframe para o Século XXI

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t cobol-one .
docker run --rm -it -v "${PWD}:/w" cobol-one bash
cobc -x capitulos/00-antes-de-comecar/OLA.cbl && ./OLA
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/OLA.cbl`

```bash
cobc -x OLA.cbl && ./OLA
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `OLA.cbl` |
| `01-o-banco-que-roda-em-1979` | `OLA.cbl`, `OLAERR1.cbl`, `OLAERR2.cbl`, `OLAEX1.cbl` |
| `03-montando-a-bancada` | `settings.json`, `build.sh` |
| `04-quatro-divisoes-e-setenta-e-duas-colunas` | `CABEC01.cbl`, `ESQUELET.cbl`, `PARAGR1.cbl`, `DISPLAY1.cbl`, `PONTO1.cbl`, `CONTIN1.cbl`, `ASPAS1.cbl`, `CARTAO1.cbl` |
| `05-dados-tem-forma` | `DADOS1.cbl`, `NIVEIS1.cbl`, `MOVEX1.cbl`, `MOVEN1.cbl`, `SALDO1.cbl`, `GRUPO1.cbl`, `EXMOVE.cbl` |
| `06-aritmetica-de-dinheiro` | `ARIT1.cbl`, `ORDEM1.cbl`, `TARIFA1.cbl`, `ROUND1.cbl`, `SIZE1.cbl`, `EDITA1.cbl`, `POUPA1.cbl` |
| `07-decidir-sem-ponto-final` | `DECIDE1.cbl`, `TARIFA2.cbl`, `NEXTSEN1.cbl`, `ABREV1.cbl`, `NIVEL88.cbl`, `EVAL1.cbl`, `CLASSE1.cbl`, `EXTIPO.cbl` |
| `08-repetir` | `PERF1.cbl`, `QUEDA1.cbl`, `ESTRUT1.cbl`, `UNTIL1.cbl`, `VARY1.cbl`, `THRU1.cbl`, `TABUADA.cbl`, `META1.cbl` |
| `09-o-primeiro-arquivo` | `dados/litcta.txt`, `LECTA01.cbl`, `NEGAT01.cbl`, `CONTAAG.cbl` |
| `10-o-arquivo-que-nao-abriu` | `FSDEMO.cbl`, `FSTAT1.cbl`, `dados/litcta-v2.txt`, `FSSAIDA.cbl` |
| `11-layouts-e-copybooks` | `dados/folha.txt`, `copy/FOLHA.cpy`, `FOLHA01.cbl`, `REDEF1.cbl`, `REDERR.cbl`, `copy/LITCTA.cpy` |
| `12-tabelas` | `TAB1.cbl`, `dados/depara.txt`, `DEPARA1.cbl`, `MESES.cbl` |
| `13-relatorio-com-quebra-de-controle` | `RELAG01.cbl` |
| `14-texto` | `CPFVAL1.cbl`, `UNSTR1.cbl`, `STRING1.cbl`, `CORTADO.cbl`, `IDCONTA.cbl` |
| `15-ordenar` | `dados/litcta-cli.txt`, `SORT1.cbl`, `SORT2.cbl` |
| `16-balance-line` | `dados/litcli.txt`, `dados/vercli.txt`, `BALAN01.cbl` |
| `17-onde-o-dinheiro-mora` | `COMP3A.cbl`, `S0C7A.cbl` |
| `18-o-arquivo-que-veio-de-santos` | `dados/litsaldo.txt`, `SINAL1.cbl` |
| `19-arquivo-indexado` | `CRIAIDX.cbl`, `CONSIDX.cbl` |
| `20-subprogramas` | `VALCPF.cbl`, `copy/VALCPFL.cpy`, `CONVVAL.cbl`, `CONTACH.cbl`, `CHAMA3.cbl`, `copy/SOMA2L.cpy`, `SOMA2.cbl`, `USASOMA.cbl`, `ALTERA.cbl`, `TESTAREF.cbl` |
| `21-datas-e-dias-uteis` | `DATAS1.cbl`, `DATAS2.cbl`, `DUTIL1.cbl`, `FALTAM.cbl` |
| `22-juros-ate-o-centavo` | `TAXAS1.cbl`, `dados/saldos-dez.txt`, `JUROS1.cbl` |
| `25-o-abend-das-duas-da-manha` | `LOOP1.cbl` |
| `28-testar-o-que-ninguem-testou` | `TESTVAL.cbl`, `dados/massa.txt`, `dados/testval-esperado.txt` |
| `29-o-fim-de-semana-da-conversao` | `copy/VERCTA.cpy`, `CONVCTA.cbl` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
