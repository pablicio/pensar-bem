       IDENTIFICATION DIVISION.
       PROGRAM-ID. NEGAT01.
      *---------------------------------------------------------------
      * GRAVA AS CONTAS DO LITORAL COM SALDO NEGATIVO
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-LITORAL ASSIGN TO LITCTA
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT ARQ-NEGATIVOS ASSIGN TO NEGAT
               ORGANIZATION IS LINE SEQUENTIAL.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
       01  LIT-REGISTRO.
           05  LIT-AGENCIA         PIC 9(4).
           05  LIT-CONTA           PIC 9(7).
           05  LIT-DIGITO          PIC X.
           05  LIT-NOME            PIC X(22).
           05  FILLER              PIC X(21).
           05  LIT-SALDO           PIC 9(11)V99.
           05  LIT-SINAL           PIC X.
           05  LIT-STATUS          PIC X.
       FD  ARQ-NEGATIVOS.
       01  NEG-REGISTRO.
           05  NEG-AGENCIA         PIC 9(4).
           05  NEG-CONTA           PIC 9(7).
           05  NEG-NOME            PIC X(22).
           05  NEG-SALDO           PIC 9(11)V99.
       WORKING-STORAGE SECTION.
       01  WS-FIM-ARQUIVO          PIC X         VALUE "N".
           88  CND-FIM-ARQUIVO                   VALUE "S".
       01  WS-LIDOS                PIC 9(9)      VALUE 0.
       01  WS-GRAVADOS             PIC 9(9)      VALUE 0.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           OPEN INPUT  ARQ-LITORAL
                OUTPUT ARQ-NEGATIVOS
           PERFORM 2100-LER
           PERFORM 2000-PROCESSAR UNTIL CND-FIM-ARQUIVO
           CLOSE ARQ-LITORAL ARQ-NEGATIVOS
           DISPLAY "LIDOS:    " WS-LIDOS
           DISPLAY "GRAVADOS: " WS-GRAVADOS
           GOBACK.
       2000-PROCESSAR.
           ADD 1 TO WS-LIDOS
           IF LIT-SINAL = "-"
               MOVE LIT-AGENCIA TO NEG-AGENCIA
               MOVE LIT-CONTA   TO NEG-CONTA
               MOVE LIT-NOME    TO NEG-NOME
               MOVE LIT-SALDO   TO NEG-SALDO
               WRITE NEG-REGISTRO
               ADD 1 TO WS-GRAVADOS
           END-IF
           PERFORM 2100-LER.
       2100-LER.
           READ ARQ-LITORAL
               AT END SET CND-FIM-ARQUIVO TO TRUE
           END-READ.
