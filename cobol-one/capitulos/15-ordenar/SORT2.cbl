       IDENTIFICATION DIVISION.
       PROGRAM-ID. SORT2.
      *---------------------------------------------------------------
      * TOTAL POR AGENCIA DAS CONTAS NAO ENCERRADAS DO LITORAL
      * ENTRADA EM QUALQUER ORDEM; ORDENA INTERNAMENTE
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
           DECIMAL-POINT IS COMMA.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-LITORAL ASSIGN TO LITCTA
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-LITORAL.
           SELECT ARQ-TRABALHO ASSIGN TO SORTWK1.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
           COPY LITCTA REPLACING ==:PFX:== BY ==LIT==.
       SD  ARQ-TRABALHO.
       01  SRT-REGISTRO.
           05  SRT-AGENCIA             PIC 9(4).
           05  SRT-SALDO               PIC S9(13)V99.
       WORKING-STORAGE SECTION.
       01  WS-FS-LITORAL               PIC XX.
           88  FS-LIT-OK                         VALUE "00".
           88  FS-LIT-FIM                        VALUE "10".
       01  WS-FIM-SORT                 PIC X     VALUE "N".
           88  CND-FIM-SORT                      VALUE "S".
       01  WS-LIDOS                    PIC 9(9)  VALUE 0.
       01  WS-LIBERADOS                PIC 9(9)  VALUE 0.
       01  WS-AGENCIA-ATUAL            PIC 9(4).
       01  WS-TOT-AGENCIA              PIC S9(13)V99.
       01  WS-ED-SALDO                 PIC -.---.---.--9,99.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           SORT ARQ-TRABALHO
               ON ASCENDING KEY SRT-AGENCIA
               INPUT PROCEDURE 1000-SELECIONAR
               OUTPUT PROCEDURE 2000-TOTALIZAR
           IF SORT-RETURN NOT = 0
               DISPLAY "SORT2 - ERRO NA ORDENACAO: " SORT-RETURN
               MOVE 12 TO RETURN-CODE
           END-IF
           DISPLAY "LIDOS: " WS-LIDOS " LIBERADOS: " WS-LIBERADOS
           GOBACK.
      *---------------------------------------------------------------
      * ENTRADA: LE O LITORAL, DESCARTA ENCERRADAS, MONTA O REGISTRO
      *---------------------------------------------------------------
       1000-SELECIONAR.
           OPEN INPUT ARQ-LITORAL
           IF NOT FS-LIT-OK
               DISPLAY "SORT2 - OPEN LITCTA STATUS " WS-FS-LITORAL
               MOVE 12 TO RETURN-CODE
               GOBACK
           END-IF
           READ ARQ-LITORAL
           PERFORM UNTIL NOT FS-LIT-OK
               ADD 1 TO WS-LIDOS
               IF LIT-STATUS NOT = "E"
                   MOVE LIT-AGENCIA TO SRT-AGENCIA
                   IF LIT-SINAL = "-"
                       COMPUTE SRT-SALDO = LIT-SALDO * -1
                   ELSE
                       MOVE LIT-SALDO TO SRT-SALDO
                   END-IF
                   RELEASE SRT-REGISTRO
                   ADD 1 TO WS-LIBERADOS
               END-IF
               READ ARQ-LITORAL
           END-PERFORM
           CLOSE ARQ-LITORAL.
      *---------------------------------------------------------------
      * SAIDA: RECEBE OS REGISTROS ORDENADOS E TOTALIZA POR AGENCIA
      *---------------------------------------------------------------
       2000-TOTALIZAR.
           PERFORM 2100-RECEBER
           IF NOT CND-FIM-SORT
               MOVE SRT-AGENCIA TO WS-AGENCIA-ATUAL
               MOVE 0 TO WS-TOT-AGENCIA
           END-IF
           PERFORM UNTIL CND-FIM-SORT
               IF SRT-AGENCIA NOT = WS-AGENCIA-ATUAL
                   PERFORM 2200-MOSTRAR-AGENCIA
                   MOVE SRT-AGENCIA TO WS-AGENCIA-ATUAL
                   MOVE 0 TO WS-TOT-AGENCIA
               END-IF
               ADD SRT-SALDO TO WS-TOT-AGENCIA
               PERFORM 2100-RECEBER
           END-PERFORM
           PERFORM 2200-MOSTRAR-AGENCIA.
       2100-RECEBER.
           RETURN ARQ-TRABALHO
               AT END SET CND-FIM-SORT TO TRUE
           END-RETURN.
       2200-MOSTRAR-AGENCIA.
           MOVE WS-TOT-AGENCIA TO WS-ED-SALDO
           DISPLAY "AGENCIA " WS-AGENCIA-ATUAL ": " WS-ED-SALDO.
