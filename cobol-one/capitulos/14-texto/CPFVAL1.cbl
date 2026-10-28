       IDENTIFICATION DIVISION.
       PROGRAM-ID. CPFVAL1.
      *---------------------------------------------------------------
      * LIMPA E VALIDA CPF (REGRA DA RECEITA FEDERAL)
      *---------------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-TESTES-DADOS.
           05  FILLER          PIC X(14) VALUE "123.456.789-09".
           05  FILLER          PIC X(14) VALUE "123.456.789-00".
           05  FILLER          PIC X(14) VALUE "111.111.111-11".
           05  FILLER          PIC X(14) VALUE "123.456.78-09".
       01  WS-TESTES REDEFINES WS-TESTES-DADOS.
           05  WS-TESTE            PIC X(14) OCCURS 4 TIMES.
       01  WS-T                    PIC 9.
       01  WS-DOC                  PIC X(14).
       01  WS-LIMPO                PIC X(14).
       01  WS-CPF REDEFINES WS-LIMPO.
           05  WS-CPF-DIG          PIC 9 OCCURS 14 TIMES.
       01  WS-I                    PIC 99.
       01  WS-J                    PIC 99.
       01  WS-SOMA                 PIC 9(4).
       01  WS-RESTO                PIC 99.
       01  WS-DV                   PIC 9.
       01  WS-RESULTADO            PIC X(30).
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM VARYING WS-T FROM 1 BY 1 UNTIL WS-T > 4
               MOVE WS-TESTE(WS-T) TO WS-DOC
               PERFORM 1000-LIMPAR
               PERFORM 2000-VALIDAR
               DISPLAY WS-DOC " -> " WS-RESULTADO
           END-PERFORM
           GOBACK.
       1000-LIMPAR.
           MOVE SPACES TO WS-LIMPO
           MOVE 0 TO WS-J
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 14
               IF WS-DOC(WS-I:1) IS NUMERIC
                   ADD 1 TO WS-J
                   MOVE WS-DOC(WS-I:1) TO WS-LIMPO(WS-J:1)
               END-IF
           END-PERFORM.
       2000-VALIDAR.
           EVALUATE TRUE
               WHEN WS-J NOT = 11
                   MOVE "INVALIDO: NAO TEM 11 DIGITOS" TO WS-RESULTADO
               WHEN WS-LIMPO(1:10) = WS-LIMPO(2:10)
                   MOVE "INVALIDO: DIGITOS REPETIDOS" TO WS-RESULTADO
               WHEN OTHER
                   PERFORM 2100-CALCULAR-DV
           END-EVALUATE.
       2100-CALCULAR-DV.
      *    PRIMEIRO DIGITO: PESOS 10 A 2 SOBRE OS 9 PRIMEIROS
           MOVE 0 TO WS-SOMA
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 9
               COMPUTE WS-SOMA =
                       WS-SOMA + WS-CPF-DIG(WS-I) * (11 - WS-I)
           END-PERFORM
           PERFORM 2200-DIGITO
           IF WS-DV NOT = WS-CPF-DIG(10)
               MOVE "INVALIDO: PRIMEIRO DV" TO WS-RESULTADO
           ELSE
      *        SEGUNDO DIGITO: PESOS 11 A 2 SOBRE OS 10 PRIMEIROS
               MOVE 0 TO WS-SOMA
               PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 10
                   COMPUTE WS-SOMA =
                           WS-SOMA + WS-CPF-DIG(WS-I) * (12 - WS-I)
               END-PERFORM
               PERFORM 2200-DIGITO
               IF WS-DV NOT = WS-CPF-DIG(11)
                   MOVE "INVALIDO: SEGUNDO DV" TO WS-RESULTADO
               ELSE
                   MOVE "VALIDO" TO WS-RESULTADO
               END-IF
           END-IF.
       2200-DIGITO.
           COMPUTE WS-RESTO = FUNCTION MOD(WS-SOMA, 11)
           IF WS-RESTO < 2
               MOVE 0 TO WS-DV
           ELSE
               COMPUTE WS-DV = 11 - WS-RESTO
           END-IF.
