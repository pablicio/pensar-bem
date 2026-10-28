       IDENTIFICATION DIVISION.
       PROGRAM-ID. MOVEX1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-NOME             PIC X(10).
       PROCEDURE DIVISION.
           MOVE "ANA" TO WS-NOME
           DISPLAY "[" WS-NOME "]"
           MOVE "BANCO VERTICE SA" TO WS-NOME
           DISPLAY "[" WS-NOME "]"
           MOVE ALL "*" TO WS-NOME
           DISPLAY "[" WS-NOME "]"
           MOVE SPACES TO WS-NOME
           DISPLAY "[" WS-NOME "]"
           GOBACK.
