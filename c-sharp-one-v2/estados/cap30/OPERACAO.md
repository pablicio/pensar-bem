# Operação

Para quem mantém a plataforma no ar. Cada procedimento foi executado pelo
menos uma vez por alguém que não o escreveu; a data está no fim de cada um.

## O que roda onde

| Peça | Onde | Como |
|---|---|---|
| API | servidor de aplicação | imagem `prefeitura-api:<versão>`, pelo `compose.yaml` |
| Migrations | servidor de aplicação | imagem `prefeitura-migracoes:<versão>`, roda antes da API |
| Banco | servidor de banco | PostgreSQL 17, banco `prefeitura` |
| E-mail | serviço de mensagens da prefeitura | `Correio:Endereco` |
| SMS | fornecedor contratado | `Sms:Endereco`, chave em `CHAVE_DO_SMS` |

Monitor: `GET /saude` responde `Healthy` quando a API fala com o banco.

## Entregar uma versão

1. Confira que o pipeline da versão está verde.
2. No servidor de aplicação, troque a etiqueta das imagens no
   `compose.yaml` (ex.: `1.0.2` → `1.0.3`).
3. `docker compose up -d` — o Compose roda as migrations e depois a API.
4. `/saude` verde.
5. Confira em produção o caminho que motivou a entrega.

Anote no registro de entregas: versão, data, hora, quem.

## Voltar uma versão

Troque a etiqueta para a anterior e `docker compose up -d`. Se a versão
nova tinha migration, a anterior pode não funcionar com o banco novo:
fale com a equipe antes de voltar.

## Backup

- De hora em hora, no servidor de banco, o `backup-da-hora.sh`, pelo
  `crontab` do usuário `postgres`:

  ```
  #!/bin/bash
  pg_dump -Fc -f "/backup/hora/prefeitura-$(date +%H).dump" prefeitura
  ```

  ```
  0 * * * *  /backup/backup-da-hora.sh
  ```

  Vinte e quatro arquivos, um por hora, cada um substituído no dia
  seguinte. Leva menos de um segundo; cada arquivo tem uns 3 MB.
- O backup da noite, às 2h, é guardado por 30 dias e copiado para o
  servidor de arquivos da Secretaria de Administração.
- **Os arquivos têm o CPF, o e-mail e o celular de todos os cidadãos.**
  Acesso só para a equipe de infraestrutura.

## Restaurar

Quando o banco de produção se perdeu ou ficou inutilizável.

1. Num servidor PostgreSQL 17, crie o banco vazio:
   `createdb -U postgres prefeitura`
   (o `pg_restore` não cria o banco; sem ele, falha com
   `database "prefeitura" does not exist`).
2. Restaure o backup mais recente:
   `pg_restore -U postgres -d prefeitura prefeitura-HH.dump`
   Num banco que já tem tabelas, o `pg_restore` não substitui nada:
   falha tabela por tabela. Restaure sempre num banco vazio.
3. Confira as contagens e o último protocolo:

   ```
   SELECT count(*), max(protocolo) FROM solicitacoes;
   ```

4. **Avance a sequência do protocolo.** Os protocolos emitidos entre o
   backup e a queda não estão no banco restaurado, mas estão nos
   comprovantes dos cidadãos. Sem este passo, a API emite de novo os
   mesmos números, para outras pessoas:

   ```
   SELECT setval('protocolo_sequencial',
       (SELECT last_value FROM protocolo_sequencial) + 1000);
   ```

   Anote o salto no livro do Protocolo Geral: "números de X a Y não
   emitidos — restauração de backup em dd/mm".
5. Aponte `ConnectionStrings__Principal` da API para o servidor e
   `docker compose up -d`.
6. `/saude` verde e um protocolo de teste, conferindo o número.
7. Avise a equipe: as solicitações feitas entre o backup e a queda
   precisam ser registradas de novo, a partir dos comprovantes e do livro.

Executado por Júlia Prado (infraestrutura) em 30/06/2027: 4,7 s para
restaurar; 31 protocolos da manhã fora do backup da noite.

## Calendário

Os feriados ficam em `Calendario:Feriados`, no `appsettings.json`.
**Até 1º de dezembro de cada ano**, a lista do ano seguinte precisa estar
numa versão entregue — nacionais, estaduais e municipais (20/01, São
Sebastião; 01/06, aniversário da cidade). Sem ela, todo prazo de janeiro
sai errado.

## Corrigir prazos de um dia

Se um dia foi tratado como útil por engano (ou o contrário), depois de
corrigir a configuração:

```
docker compose run --rm api recalcular-prazos AAAA-MM-DD <matrícula>
```

Corrige os prazos dos protocolos daquele dia, deixa registro no histórico
de cada solicitação e avisa quem tem e-mail ou celular. Pode rodar duas
vezes. A matrícula é de quem autorizou a correção.

## Chaves

| Chave | Onde | Para trocar |
|---|---|---|
| `CHAVE_DOS_TOKENS` | `.env` do servidor de aplicação | gerar 32+ caracteres, trocar, `docker compose up -d`; todos os servidores entram de novo |
| `CHAVE_DO_SMS` | `.env` do servidor de aplicação | o fornecedor emite; trocar e `docker compose up -d` |
| chaves de API dos clientes | `Api:Clientes` (só o hash) | `dotnet run -- nova-chave`, novo hash numa versão, chave nova ao cliente |

## Contatos

Núcleo de Governo Digital, 2º andar do Paço: André (líder técnico),
Carla, Bruno. Infraestrutura: Wagner, Júlia. Regras de prazo: Helena Duarte
(Administração). Protocolo Geral: Paulo.
