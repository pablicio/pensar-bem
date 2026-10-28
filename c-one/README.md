# Materiais — C One: Do zero ao básico em sistemas embarcados e IoT

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t c-one .
docker run --rm -it -v "${PWD}:/projeto" c-one bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/ola.c`

```bash
gcc -o programa ola.c && ./programa
```

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `ola.c` |
| `01-voce-tem-certeza-que-isso-e-c` | `leitura.c`, `alarme.c` |
| `03-o-programa-comeca-no-main` | `vazio.c`, `tanque47.c`, `leituras.c` |
| `04-variaveis-nao-sao-caixas-magicas` | `variaveis.c`, `letra.c`, `tamanhos.c`, `limites.c`, `volta.c`, `converte.c` |
| `05-quando-o-programa-precisa-decidir` | `alarme1.c`, `alarme2.c`, `alarme3.c`, `status.c` |
| `06-repetir-e-facil-saber-quando-parar-e-outra-coisa` | `resfria.c`, `tanques.c`, `sms.c`, `continue.c` |
| `07-a-funcao-que-cresceu-demais` | `regras.c`, `zerar.c` |
| `08-onde-o-dado-realmente-esta` | `endereco.c`, `vizinhas.c`, `pilha.c` |
| `09-o-simbolo-que-parece-pequeno-demais` | `ponteiro.c`, `zerar.c`, `leitura.c`, `digita.c` |
| `10-o-bug-que-desaparece-quando-voce-coloca-um-printf` | `lixo.c`, `status.c` |
| `11-vinte-e-quatro-leituras` | `horas.c`, `maxima.c`, `contiguo.c`, `t213.c`, `funcao.c` |
| `12-strings-nao-sao-strings` | `tamanho.c`, `medir.c`, `sms1.c`, `sms2.c` |
| `13-o-tanque-vira-um-tipo` | `struct.c`, `cadastro.c`, `atualiza.c` |
| `14-o-arquivo-de-onze-mil-linhas` | `tanque.h`, `tanque.c`, `main.c`, `alarme.c`, `alarme.h` |
| `15-antes-de-compilar-outra-coisa-acontece` | `pre.c`, `macro.c`, `modem.c` |
| `16-eu-nao-vou-compilar-37-arquivos-na-mao` | `Makefile` |
| `17-o-programa-precisa-de-mais-memoria` | `malloc.c`, `cadastro.c`, `cresce.c` |
| `18-quem-esqueceu-de-dar-free` | `leitura.c`, `depois.c` |
| `19-a-cooperativa-precisa-lembrar` | `grava.c`, `le.c`, `cem.c`, `historico.h`, `consulta.c` |
| `20-o-programa-falhou-mas-por-que` | `motivo.c`, `historico.c`, `valida.c` |
| `21-o-programa-recebe-ordens` | `args.c`, `numero.c`, `opcoes.c` |
| `22-o-programa-esta-mentindo-para-voce` | `media.c` |
| `23-funciona-na-minha-maquina` | `tests/test_regras.c` |
| `24-o-codigo-dentro-da-caixinha` | `bits.c`, `status.h`, `mascaras.c`, `negativo.c` |
| `25-dois-kilobytes-de-ram` | `fila.h`, `fila.c`, `teste_fila.c` |
| `26-doze-bytes` | `ordem.c`, `pacote.c`, `pacote.h`, `teste_pacote.c` |
| `27-o-gateway-atende-o-telefone` | `servidor.c`, `rede.c`, `caixinha.c` |
| `28-duzentas-e-doze-caixinhas-ao-mesmo-tempo` | `threads.c`, `servidor.c`, `registro.c` |
| `29-a-falha-das-3h17` | `relatorio.c`, `tests/test_relatorio.c` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
