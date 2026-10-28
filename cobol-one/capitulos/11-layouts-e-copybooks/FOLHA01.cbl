       IDENTIFICATION DIVISION.
       PROGRAM-ID. FOLHA01.
      *---------------------------------------------------------------
      * LE A REMESSA DE SALARIOS E CONFERE O TRAILER
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
           DECIMAL-POINT IS COMMA.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-FOLHA ASSIGN TO FOLHA
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-FOLHA.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-FOLHA.
           COPY FOLHA REPLACING ==:PFX:== BY ==FOL==.
       WORKING-STORAGE SECTION.
       01  WS-FS-FOLHA             PIC XX.
           88  FS-FOL-OK                         VALUE "00".
           88  FS-FOL-FIM                        VALUE "10".
       01  WS-QTD-DETALHES         PIC 9(6)      VALUE 0.
       01  WS-SOMA-VALORES         PIC 9(13)V99  VALUE 0.
       01  WS-ED-VALOR             PIC ZZ.ZZZ.ZZZ.ZZ9,99.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           OPEN INPUT ARQ-FOLHA
           IF NOT FS-FOL-OK
               DISPLAY "FOLHA01 - OPEN FOLHA STATUS " WS-FS-FOLHA
               MOVE 12 TO RETURN-CODE
               GOBACK
           END-IF
           PERFORM 2100-LER
           PERFORM 2000-PROCESSAR UNTIL FS-FOL-FIM
           CLOSE ARQ-FOLHA
           GOBACK.
       2000-PROCESSAR.
           EVALUATE FOL-H-TIPO
               WHEN "0"
                   DISPLAY "EMPRESA: " FOL-H-EMPRESA
                   DISPLAY "CREDITO: " FOL-H-DATA-CREDITO
               WHEN "1"
                   ADD 1 TO WS-QTD-DETALHES
                   ADD FOL-D-VALOR TO WS-SOMA-VALORES
                   MOVE FOL-D-VALOR TO WS-ED-VALOR
                   DISPLAY FOL-D-AGENCIA "-" FOL-D-CONTA " "
                           FOL-D-NOME WS-ED-VALOR
               WHEN "9"
                   PERFORM 2200-CONFERIR-TRAILER
               WHEN OTHER
                   DISPLAY "TIPO DE REGISTRO INVALIDO: " FOL-H-TIPO
           END-EVALUATE
           PERFORM 2100-LER.
       2100-LER.
           READ ARQ-FOLHA
           IF NOT FS-FOL-OK AND NOT FS-FOL-FIM
               DISPLAY "FOLHA01 - READ FOLHA STATUS " WS-FS-FOLHA
               MOVE 12 TO RETURN-CODE
               SET FS-FOL-FIM TO TRUE
           END-IF.
       2200-CONFERIR-TRAILER.
           IF FOL-T-QTD = WS-QTD-DETALHES
              AND FOL-T-TOTAL = WS-SOMA-VALORES
               MOVE WS-SOMA-VALORES TO WS-ED-VALOR
               DISPLAY "TRAILER CONFERE: " FOL-T-QTD " CREDITOS,"
                       " TOTAL" WS-ED-VALOR
           ELSE
               DISPLAY "TRAILER NAO CONFERE"
               MOVE 12 TO RETURN-CODE
           END-IF.
