       IDENTIFICATION DIVISION.
       PROGRAM-ID. CONTAAG.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-LITORAL ASSIGN TO LITCTA
               ORGANIZATION IS LINE SEQUENTIAL.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
       01  LIT-REGISTRO.
           05  LIT-AGENCIA         PIC 9(4).
           05  FILLER              PIC X(66).
       WORKING-STORAGE SECTION.
       01  WS-FIM-ARQUIVO          PIC X         VALUE "N".
           88  CND-FIM-ARQUIVO                   VALUE "S".
       01  WS-QTD-0101             PIC 9(9)      VALUE 0.
       01  WS-QTD-0102             PIC 9(9)      VALUE 0.
       01  WS-QTD-0205             PIC 9(9)      VALUE 0.
       01  WS-QTD-OUTRAS           PIC 9(9)      VALUE 0.
       PROCEDURE DIVISION.
           OPEN INPUT ARQ-LITORAL
           PERFORM 2100-LER
           PERFORM UNTIL CND-FIM-ARQUIVO
               EVALUATE LIT-AGENCIA
                   WHEN 0101  ADD 1 TO WS-QTD-0101
                   WHEN 0102  ADD 1 TO WS-QTD-0102
                   WHEN 0205  ADD 1 TO WS-QTD-0205
                   WHEN OTHER ADD 1 TO WS-QTD-OUTRAS
               END-EVALUATE
               PERFORM 2100-LER
           END-PERFORM
           CLOSE ARQ-LITORAL
           DISPLAY "0101: " WS-QTD-0101
           DISPLAY "0102: " WS-QTD-0102
           DISPLAY "0205: " WS-QTD-0205
           DISPLAY "OUTRAS: " WS-QTD-OUTRAS
           GOBACK.
       2100-LER.
           READ ARQ-LITORAL
               AT END SET CND-FIM-ARQUIVO TO TRUE
           END-READ.
