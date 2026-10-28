# Materiais — JavaScript One: Do primeiro console.log ao painel em produção

Arquivos para acompanhar o livro: exemplos, projeto e o ambiente Docker.
O e-book em si não entra neste zip.

## Como executar

Descompacte o zip e abra a pasta no terminal. Com o Docker instalado e aberto:

```bash
docker build -t javascript-one .
docker run --rm -it -v "${PWD}:/projeto" javascript-one bash
```

No PowerShell o volume é `"${PWD}:/projeto"` (ou `/livro` no Assembly One).

Cada capítulo do livro tem uma pasta em `capitulos/`. Entre na pasta do
capítulo que está lendo e rode o arquivo. O primeiro é:

`capitulos/00-antes-de-comecar/status.js`

```bash
node status.js
```

## Projeto final

`projeto-final/` junta a última versão completa de cada arquivo do
sistema que o livro constrói. Recortes didáticos ficam só em
`capitulos/`. Como executar: abra `projeto-final/README.md`.

## O que tem neste pacote

- `capitulos/` — um arquivo por exemplo, na ordem do livro
- `Dockerfile`
- `projeto-final/ (19 arquivos)`

### Arquivos por capítulo

| Capítulo | Arquivos |
|---|---|
| `00-antes-de-comecar` | `status.js` |
| `02-o-que-vamos-construir` | `package.json` |
| `03-primeiro-programa` | `status.js`, `anda.js`, `quebra.js`, `nome.js` |
| `04-variaveis-e-tipos` | `tipos.js`, `ausencia.js`, `conversao.js`, `comparacao.js`, `pendencias.js`, `frete.js` |
| `05-operadores` | `contas.js`, `frete.js`, `comparar.js`, `ou.js`, `precedencia.js` |
| `06-condicionais` | `rotulo.js`, `situacao.js`, `cor.js` |
| `07-repeticoes` | `lista.js`, `tentativas.js`, `totais.js`, `franca.js` |
| `08-funcoes` | `dobro.js`, `entrega.js`, `frete.js`, `confere.js` |
| `09-escopo` | `bloco.js`, `laco.js`, `notifica.js`, `sombra.js` |
| `10-arrays-e-objetos` | `entrega.js`, `manha.js`, `normalizar.js` |
| `11-desestruturacao-e-spread` | `mesmo.js`, `copia.js`, `raso.js`, `frete.js` |
| `12-callbacks` | `avisar.js`, `espera.js`, `status.js` |
| `13-promises` | `promessa.js`, `tela.js` |
| `14-async-await` | `linha.js`, `tela.js`, `urgente.js` |
| `15-closures` | `contador.js`, `botoes.js`, `rodada.js` |
| `16-dom-e-eventos` | `index.html`, `painel.js` |
| `17-debugging` | `lista.css` |
| `18-estado` | `duas-copias.js`, `estado.js`, `painel.js` |
| `19-modulos` | `frete.js`, `painel.js`, `package.json`, `entrega.js`, `lista.js`, `situacoes.js` |
| `20-npm` | `package.json`, `package-lock.json`, `entrega.js`, `endereco.js`, `api.js`, `confere-http.js` |
| `21-testes` | `test/frete.test.js`, `package.json`, `painel.js`, `test/intervalo.test.js` |
| `22-apis` | `servidor.js`, `cliente.js`, `api.js` |
| `23-performance` | `relogio.js`, `painel.js` |
| `24-git` | `.gitignore`, `frete.js` |
| `25-deploy` | `rodape.js`, `package.json` |
| `26-projeto-final` | `conferencia.js` |

Se um arquivo aparece em mais de um capítulo, a pasta de cada capítulo
guarda a versão daquele ponto do livro.

Fonte: Editora Pensar Bem · pensarbem.com.br/materiais/livros
