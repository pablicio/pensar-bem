       IDENTIFICATION DIVISION.
       PROGRAM-ID. EVAL1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-TIPO-CONTA       PIC X(2)      VALUE "PJ".
       01  WS-SALDO-MEDIO      PIC S9(9)V99  VALUE 12000.00.
       01  WS-TARIFA           PIC S9(3)V99.
       PROCEDURE DIVISION.
           EVALUATE TRUE
               WHEN WS-TIPO-CONTA = "PF" AND WS-SALDO-MEDIO >= 5000
                   MOVE 0 TO WS-TARIFA
               WHEN WS-TIPO-CONTA = "PF"
                   MOVE 19.90 TO WS-TARIFA
               WHEN WS-TIPO-CONTA = "PJ" AND WS-SALDO-MEDIO >= 50000
                   MOVE 39.90 TO WS-TARIFA
               WHEN WS-TIPO-CONTA = "PJ"
                   MOVE 79.90 TO WS-TARIFA
               WHEN OTHER
                   DISPLAY "TIPO DE CONTA INVALIDO: " WS-TIPO-CONTA
                   MOVE 0 TO WS-TARIFA
           END-EVALUATE
           DISPLAY "TARIFA: " WS-TARIFA
           GOBACK.
