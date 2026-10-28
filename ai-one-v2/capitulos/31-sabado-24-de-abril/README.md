# Rateio da Coopersol Cerrado

O rateio de créditos das três usinas, do dado bruto ao
arquivo da GED. Versão 0.3.0.

## Todo mês, até o dia 5

1. Copie os arquivos novos dos inversores e da GED para
   `dados/brutos/`, nas mesmas pastas dos outros.
2. Abra o terminal do contêiner na pasta do projeto.
3. Atualize o manifesto: `python manifesto_brutos.py`.
4. Rode: `sh rodar.sh AAAA-MM` (o mês que acabou).
5. Confira a última linha: tem de ser `INFO    pronto`.
6. Envie `resultados/AAAA-MM/envio_ged_AAAA-MM.csv` pelo
   portal da GED e grampeie o protocolo no log impresso.

## Se aparecer ERROR

- `alterado:` um arquivo bruto mudou depois do manifesto.
  Não mexa em nada e avise a Tainá.
- `mudou de colunas`: um fabricante mudou o formato.
  Não envie nada e avise a Tainá.
- um teste falhou (`F` na linha de pontos): não envie nada.

## Onde está cada coisa

- `rateio/`: o pacote, com as regras; `tests/`: os testes.
- `rateio.toml`: pastas e tarifa (a tarifa muda em janeiro).
- `resultados/AAAA-MM/`: envio, origem e log de cada mês.
- `experimentos/registro.csv`: as comparações de regras.
