       IDENTIFICATION DIVISION.
       PROGRAM-ID. SIZE1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-CONTADOR         PIC S9(3)     VALUE 999.
       01  WS-A                PIC S9(3)     VALUE 10.
       01  WS-ZERO             PIC S9(3)     VALUE 0.
       01  WS-R                PIC S9(3)     VALUE 7.
       PROCEDURE DIVISION.
           ADD 1 TO WS-CONTADOR
               ON SIZE ERROR
                   DISPLAY "NAO CABE. CONTADOR = " WS-CONTADOR
               NOT ON SIZE ERROR
                   DISPLAY "SOMOU"
           END-ADD
           ADD 1 TO WS-CONTADOR
           DISPLAY "SEM SIZE ERROR, CONTADOR = " WS-CONTADOR
           DIVIDE WS-A BY WS-ZERO GIVING WS-R
               ON SIZE ERROR
                   DISPLAY "DIVISAO POR ZERO. R = " WS-R
           END-DIVIDE
           GOBACK.
