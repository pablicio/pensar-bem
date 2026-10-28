       IDENTIFICATION DIVISION.
       PROGRAM-ID. EXMOVE.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-R                PIC 9(3)V9.
       01  WS-T                PIC X(5).
       PROCEDURE DIVISION.
           MOVE 12.345 TO WS-R
           DISPLAY "[" WS-R "]"
           MOVE 1234.5 TO WS-R
           DISPLAY "[" WS-R "]"
           MOVE "CONTA CORRENTE" TO WS-T
           DISPLAY "[" WS-T "]"
           MOVE 42 TO WS-T
           DISPLAY "[" WS-T "]"
           GOBACK.
