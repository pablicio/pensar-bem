       IDENTIFICATION DIVISION.
       PROGRAM-ID. MOVEN1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-VALOR            PIC 9(5)V99.
       01  WS-INTEIRO          PIC 9(4).
       01  WS-COM-SINAL        PIC S9(3)V99  VALUE -12.34.
       PROCEDURE DIVISION.
           MOVE 7 TO WS-VALOR
           DISPLAY "7          -> " WS-VALOR
           MOVE 123.4 TO WS-VALOR
           DISPLAY "123.4      -> " WS-VALOR
           MOVE 1.987 TO WS-VALOR
           DISPLAY "1.987      -> " WS-VALOR
           MOVE 1234567.89 TO WS-VALOR
           DISPLAY "1234567.89 -> " WS-VALOR
           MOVE WS-COM-SINAL TO WS-INTEIRO
           DISPLAY "-12.34     -> " WS-INTEIRO
           GOBACK.
