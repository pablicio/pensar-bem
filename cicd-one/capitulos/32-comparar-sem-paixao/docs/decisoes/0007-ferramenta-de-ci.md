# 0007 — GitHub Actions como ferramenta de CI/CD

Data: 2027-05-07. Situação: aceita.

## Contexto
Pilotos com o mesmo pipeline em GitHub Actions, GitLab CI,
CircleCI e Jenkins (planilha em docs/pilotos/).

## Decisão
GitHub Actions. Builds de iOS no Mac mini, runner próprio.

## Consequências
- Sem servidor de CI para manter; custo ~US$ 20/mês.
- Dependemos do GitHub para código e pipeline.
- Pipeline fino: o trabalho fica no Makefile e em scripts,
  o que mantém a troca possível.

## Rever quando
- mudarmos o código de plataforma; ou
- o custo em minutos passar de US$ 150/mês; ou
- em maio de 2028.
