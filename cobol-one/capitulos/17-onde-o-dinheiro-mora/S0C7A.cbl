       IDENTIFICATION DIVISION.
       PROGRAM-ID. S0C7A.
      *---------------------------------------------------------------
      * UM CAMPO COMP-3 QUE RECEBEU ESPACOS
      *---------------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-REGISTRO.
           05  WS-VALOR            PIC S9(5)V99  COMP-3.
       01  WS-REGISTRO-X REDEFINES WS-REGISTRO  PIC X(4).
       01  WS-TOTAL                PIC S9(9)V99  COMP-3 VALUE 0.
       PROCEDURE DIVISION.
           MOVE SPACES TO WS-REGISTRO-X
           DISPLAY "SOMANDO O VALOR NO TOTAL"
           ADD WS-VALOR TO WS-TOTAL
           DISPLAY "TOTAL: " WS-TOTAL
           GOBACK.
