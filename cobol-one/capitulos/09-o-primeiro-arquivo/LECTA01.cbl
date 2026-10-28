       IDENTIFICATION DIVISION.
       PROGRAM-ID. LECTA01.
      *---------------------------------------------------------------
      * LE O ARQUIVO DE CONTAS DO LITORAL E MOSTRA CADA CONTA
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
           DECIMAL-POINT IS COMMA.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-LITORAL ASSIGN TO LITCTA
               ORGANIZATION IS LINE SEQUENTIAL.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
       01  LIT-REGISTRO.
           05  LIT-AGENCIA         PIC 9(4).
           05  LIT-CONTA           PIC 9(7).
           05  LIT-DIGITO          PIC X.
           05  LIT-NOME            PIC X(22).
           05  LIT-DOCUMENTO       PIC X(14).
           05  LIT-TIPO-PESSOA     PIC X.
           05  LIT-DATA-ABERTURA   PIC 9(6).
           05  LIT-SALDO           PIC 9(11)V99.
           05  LIT-SINAL           PIC X.
           05  LIT-STATUS          PIC X.
       WORKING-STORAGE SECTION.
       01  WS-FIM-ARQUIVO          PIC X         VALUE "N".
           88  CND-FIM-ARQUIVO                   VALUE "S".
       01  WS-LIDOS                PIC 9(9)      VALUE 0.
       01  WS-SALDO                PIC S9(13)V99 VALUE 0.
       01  WS-TOTAL                PIC S9(13)V99 VALUE 0.
       01  WS-ED-SALDO             PIC -.---.---.--9,99.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM 1000-INICIALIZAR
           PERFORM 2000-PROCESSAR UNTIL CND-FIM-ARQUIVO
           PERFORM 3000-FINALIZAR
           GOBACK.
       1000-INICIALIZAR.
           OPEN INPUT ARQ-LITORAL
           PERFORM 2100-LER.
       2000-PROCESSAR.
           ADD 1 TO WS-LIDOS
           IF LIT-SINAL = "-"
               COMPUTE WS-SALDO = LIT-SALDO * -1
           ELSE
               MOVE LIT-SALDO TO WS-SALDO
           END-IF
           ADD WS-SALDO TO WS-TOTAL
           MOVE WS-SALDO TO WS-ED-SALDO
           DISPLAY LIT-AGENCIA "-" LIT-CONTA "-" LIT-DIGITO " "
                   LIT-NOME WS-ED-SALDO
           PERFORM 2100-LER.
       2100-LER.
           READ ARQ-LITORAL
               AT END
                   SET CND-FIM-ARQUIVO TO TRUE
           END-READ.
       3000-FINALIZAR.
           CLOSE ARQ-LITORAL
           MOVE WS-TOTAL TO WS-ED-SALDO
           DISPLAY "CONTAS LIDAS: " WS-LIDOS
           DISPLAY "SALDO TOTAL:  " WS-ED-SALDO.
