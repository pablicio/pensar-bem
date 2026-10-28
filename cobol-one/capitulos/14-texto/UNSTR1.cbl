       IDENTIFICATION DIVISION.
       PROGRAM-ID. UNSTR1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-LINHA                PIC X(40)
                                   VALUE "0101;SANTOS CENTRO;0412;SP".
       01  WS-AG-LITORAL           PIC X(4).
       01  WS-NOME                 PIC X(20).
       01  WS-AG-VERTICE           PIC X(4).
       01  WS-UF                   PIC X(2).
       01  WS-QTD-CAMPOS           PIC 9.
       PROCEDURE DIVISION.
           MOVE 0 TO WS-QTD-CAMPOS
           UNSTRING WS-LINHA DELIMITED BY ";"
               INTO WS-AG-LITORAL WS-NOME WS-AG-VERTICE WS-UF
               TALLYING IN WS-QTD-CAMPOS
               ON OVERFLOW
                   DISPLAY "MAIS CAMPOS DO QUE O ESPERADO"
           END-UNSTRING
           DISPLAY "[" WS-AG-LITORAL "][" WS-NOME "]["
                   WS-AG-VERTICE "][" WS-UF "] CAMPOS: " WS-QTD-CAMPOS
           GOBACK.
