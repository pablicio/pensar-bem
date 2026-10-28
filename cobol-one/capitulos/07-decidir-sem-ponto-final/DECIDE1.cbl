       IDENTIFICATION DIVISION.
       PROGRAM-ID. DECIDE1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-SALDO            PIC S9(7)V99  VALUE -350.00.
       01  WS-LIMITE           PIC S9(7)V99  VALUE 1000.00.
       PROCEDURE DIVISION.
           IF WS-SALDO < 0
               DISPLAY "CONTA NO CHEQUE ESPECIAL"
               IF WS-SALDO < WS-LIMITE * -1
                   DISPLAY "LIMITE ESTOURADO"
               ELSE
                   DISPLAY "DENTRO DO LIMITE"
               END-IF
           ELSE
               DISPLAY "SALDO POSITIVO"
           END-IF
           DISPLAY "FIM DA ANALISE"
           GOBACK.
