       IDENTIFICATION DIVISION.
       PROGRAM-ID. ESTRUT1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-CONTADOR         PIC 9(5)      VALUE 0.
       01  WS-FIM              PIC X         VALUE "N".
           88  CND-FIM                       VALUE "S".
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM 1000-INICIALIZAR
           PERFORM 2000-PROCESSAR UNTIL CND-FIM
           PERFORM 3000-FINALIZAR
           GOBACK.
      *---------------------------------------------------------------
       1000-INICIALIZAR.
           DISPLAY "1000: ABRE ARQUIVOS, ZERA TOTAIS"
           MOVE 0 TO WS-CONTADOR.
      *---------------------------------------------------------------
       2000-PROCESSAR.
           ADD 1 TO WS-CONTADOR
           DISPLAY "2000: PROCESSA O REGISTRO " WS-CONTADOR
           IF WS-CONTADOR = 3
               SET CND-FIM TO TRUE
           END-IF.
      *---------------------------------------------------------------
       3000-FINALIZAR.
           DISPLAY "3000: FECHA ARQUIVOS, TOTAIS: " WS-CONTADOR.
