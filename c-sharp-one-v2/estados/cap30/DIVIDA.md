# Dívida técnica

O que sabemos que está aquém do que deveria, por que ficou assim, quem
responde e até quando. Revista inteira em 30/06/2027, na entrega do
convênio. Linha fechada fica riscada, com a data e o que a fechou.

## Abertas

- 2027-04-06 · O aviso ao cidadão é enviado dentro do pedido de protocolo
  e espera o serviço de mensagens (até 4 s)
  motivo: mandar depois exige fila e operação próprias · dono: André,
  Wagner · prioridade: quando o antivírus do serviço de mensagens não
  puder ser ajustado

- 2027-05-03 · Token de servidor vale 8 h e não pode ser revogado;
  `Ativo` só é conferido no login
  motivo: simplicidade no lançamento · dono: Carla · prioridade: antes de
  integrar outro órgão

- 2027-06-01 · O banco não guarda quando a solicitação foi protocolada,
  só quando foi criada
  motivo: não fazia falta até o recálculo de prazos · dono: Carla ·
  prioridade: próxima versão com migration

- 2027-06-30 · `Atendimento` usa `DateTime.UtcNow`; o histórico não passa
  pelo `TimeProvider` e a hora dele não é testável
  motivo: o `TimeProvider` chegou depois do histórico · dono: Carla ·
  prioridade: junto com a anterior

## Fechadas

- ~~2027-02-04 · API devolve as entidades inteiras (CPF exposto)~~
  fechada em 2027-03-10: contratos em records, mapeamento explícito

- ~~2027-03-01 · A sequência do protocolo pode pular números~~
  fechada em 2027-06-30: o salto é esperado (pedido que falha, restauração
  de backup) e fica anotado no livro do Protocolo Geral · Paulo

- ~~2027-03-08 · Protocolar de novo e cancelar encerrada respondem `500`~~
  fechada em 2027-04-19: `RegraDeNegocioException` e `409`

- ~~2027-03-08 · DELETE de solicitação aberto na API~~
  fechada em 2027-04-26: endpoint removido; responde `405`

- ~~2027-03-12 · Erro de validação sai em dois formatos~~
  fechada em 2027-03-17: `ProblemDetails` em todos

- ~~2027-06-01 · O log de produção grava cada comando SQL~~
  fechada em 2027-06-08 (1.0.3): `Warning` para o EF Core em produção
