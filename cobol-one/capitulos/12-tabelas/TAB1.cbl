       IDENTIFICATION DIVISION.
       PROGRAM-ID. TAB1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-MESES-DADOS.
           05  FILLER              PIC X(9)      VALUE "JANEIRO".
           05  FILLER              PIC X(9)      VALUE "FEVEREIRO".
           05  FILLER              PIC X(9)      VALUE "MARCO".
       01  WS-MESES REDEFINES WS-MESES-DADOS.
           05  WS-MES-NOME         PIC X(9) OCCURS 3 TIMES.
       01  WS-OUTRO                PIC X(9)      VALUE "OUTRO".
       01  WS-I                    PIC 9(2).
       PROCEDURE DIVISION.
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 3
               DISPLAY WS-I " " WS-MES-NOME(WS-I)
           END-PERFORM
           MOVE 4 TO WS-I
           MOVE "XXXXXXXXX" TO WS-MES-NOME(WS-I)
           DISPLAY "OUTRO AGORA: [" WS-OUTRO "]"
           GOBACK.
