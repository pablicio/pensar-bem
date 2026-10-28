       IDENTIFICATION DIVISION.
       PROGRAM-ID. VALCPF.
      *---------------------------------------------------------------
      * VALCPF - VALIDA CPF (REGRA DA RECEITA FEDERAL)
      * ENTRADA: LK-DOCUMENTO, CPF COM OU SEM FORMATACAO
      * SAIDA:   LK-RETORNO  "00" VALIDO
      *                      "01" NAO TEM 11 DIGITOS
      *                      "02" DIGITOS REPETIDOS
      *                      "03" DIGITO VERIFICADOR ERRADO
      *          LK-CPF-NUMERICO, OS 11 DIGITOS (SE VALIDO)
      *---------------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-LIMPO                PIC X(14).
       01  WS-CPF REDEFINES WS-LIMPO.
           05  WS-CPF-DIG          PIC 9 OCCURS 14 TIMES.
       01  WS-I                    PIC 99.
       01  WS-J                    PIC 99.
       01  WS-SOMA                 PIC 9(4).
       01  WS-RESTO                PIC 99.
       01  WS-DV                   PIC 9.
       LINKAGE SECTION.
           COPY VALCPFL.
       PROCEDURE DIVISION USING LK-VALCPF.
       0000-PRINCIPAL.
           MOVE ZEROS TO LK-CPF-NUMERICO
           PERFORM 1000-LIMPAR
           EVALUATE TRUE
               WHEN WS-J NOT = 11
                   MOVE "01" TO LK-RETORNO
               WHEN WS-LIMPO(1:10) = WS-LIMPO(2:10)
                   MOVE "02" TO LK-RETORNO
               WHEN OTHER
                   PERFORM 2000-CALCULAR-DV
           END-EVALUATE
           GOBACK.
       1000-LIMPAR.
           MOVE SPACES TO WS-LIMPO
           MOVE 0 TO WS-J
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 14
               IF LK-DOCUMENTO(WS-I:1) IS NUMERIC
                   ADD 1 TO WS-J
                   IF WS-J <= 14
                       MOVE LK-DOCUMENTO(WS-I:1) TO WS-LIMPO(WS-J:1)
                   END-IF
               END-IF
           END-PERFORM.
       2000-CALCULAR-DV.
           MOVE 0 TO WS-SOMA
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 9
               COMPUTE WS-SOMA =
                       WS-SOMA + WS-CPF-DIG(WS-I) * (11 - WS-I)
           END-PERFORM
           PERFORM 2100-DIGITO
           IF WS-DV NOT = WS-CPF-DIG(10)
               MOVE "03" TO LK-RETORNO
           ELSE
               MOVE 0 TO WS-SOMA
               PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 10
                   COMPUTE WS-SOMA =
                           WS-SOMA + WS-CPF-DIG(WS-I) * (12 - WS-I)
               END-PERFORM
               PERFORM 2100-DIGITO
               IF WS-DV NOT = WS-CPF-DIG(11)
                   MOVE "03" TO LK-RETORNO
               ELSE
                   MOVE "00" TO LK-RETORNO
                   MOVE WS-LIMPO(1:11) TO LK-CPF-NUMERICO
               END-IF
           END-IF.
       2100-DIGITO.
           COMPUTE WS-RESTO = FUNCTION MOD(WS-SOMA, 11)
           IF WS-RESTO < 2
               MOVE 0 TO WS-DV
           ELSE
               COMPUTE WS-DV = 11 - WS-RESTO
           END-IF.
