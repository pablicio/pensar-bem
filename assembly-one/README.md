# Materiais — Assembly One: Do zero ao RISC-V

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t assembly-one:riscv docker
docker run -it --rm -v "${PWD}:/livro" assembly-one:riscv bash
# dentro do contêiner: roda capitulos/00-antes-de-comecar/leitos.s
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/Dockerfile`

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `docker/ (4 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `Dockerfile`, `leitos.s` |
| `01-o-hospital-tem-um-problema` | `leitos.s`, `roda`, `semfim.s`, `uti.s`, `leitos94.s` |
| `03-conhecendo-o-risc-v` | `leitos3.s` |
| `04-hello-hospital` | `oi.s`, `display`, `leitos.s`, `maximo.s`, `erro1.s`, `erro2.s`, `erro3.s`, `ps.s` |
| `05-memoria-nao-e-banco-de-dados` | `disponiveis.s`, `atualizar.s`, `uti.s`, `duas-alas.s` |
| `06-trinta-e-dois-registradores` | `livres.s`, `livres-a0.s`, `refeicoes.s`, `refeicoes2.s`, `conferencia.s` |
| `07-se-houver-leito-interne` | `admitir.s`, `admitir0.s`, `imediato.s`, `admitir-sem-j.s`, `lotado.s`, `dois.s` |
| `08-o-computador-nao-sabe-o-que-voce-quis-dizer` | `livres71.s`, `sem-la.s`, `depura`, `livres.s`, `livres-add.s`, `livres-sanidade.s` |
| `09-o-dia-em-que-o-hospital-descobriu-o-loop` | `semana.s`, `semana-sem-passo.s`, `semana-depois.s`, `semana-zero.s`, `contagem.s`, `quinzenas.s` |
| `10-fila-de-pacientes` | `fila.s`, `chegada.s`, `chegadas.s`, `soma-espera.s`, `chegadas-limite.s` |
| `11-prioridade` | `prioridade.s`, `empate.s`, `empate-bgt.s`, `maior-espera.s` |
| `12-tres-da-manha` | `noite.s`, `noite-depuracao.s`, `noite45.s` |
| `13-dezesseis-bits` | `ano.s`, `ano-lhu.s`, `setenta-mil.s`, `saida300.s`, `contador.s`, `menos40.s`, `contador-milhao.s` |
| `14-o-paciente-chegou` | `tecla.s`, `eco.s`, `plantao.s`, `painel.s`, `painel-sanidade.s` |
| `15-triagem` | `triagem.s`, `triagem-bruno.s` |
| `16-vamos-fazer-o-sistema` | `menu.s`, `menu-sem-faixa.s` |
| `17-dividindo-o-problema` | `sub.s`, `livres-sub.s`, `mostra-livres.s`, `refeicoes-sub.s`, `fatorial.s` |
| `18-o-turno-da-noite` | `painel-v1.s` |
| `19-o-que-acontece-num-load` | `teclas.txt` |
| `20-uma-instrucao-uma-viagem` | `teclas4.txt` |
| `21-so-falta-testar` | `testes.sh`, `painel-v2.s` |
| `22-o-codigo-que-ninguem-quer-mexer` | `painel_v0.s`, `painel_v0_nop.s`, `painel_v0_legivel.s` |
| `23-assembly-nao-era-sobre-assembly` | `livres.c`, `soma.c` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
