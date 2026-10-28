       IDENTIFICATION DIVISION.
       PROGRAM-ID. RELAG01.
      *---------------------------------------------------------------
      * RELATORIO DE SALDOS DO LITORAL COM QUEBRA POR AGENCIA
      * ENTRADA: LITCTA ORDENADO POR AGENCIA E CONTA
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
           SELECT ARQ-RELAT ASSIGN TO RELAT
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-RELAT.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
           COPY LITCTA REPLACING ==:PFX:== BY ==LIT==.
       FD  ARQ-RELAT.
       01  REL-LINHA                   PIC X(70).
       WORKING-STORAGE SECTION.
       01  WS-FS-LITORAL               PIC XX.
           88  FS-LIT-OK                         VALUE "00".
           88  FS-LIT-FIM                        VALUE "10".
       01  WS-FS-RELAT                 PIC XX.
           88  FS-REL-OK                         VALUE "00".
       01  WS-CONTROLE.
           05  WS-AGENCIA-ATUAL        PIC 9(4).
           05  WS-LINHAS-NA-PAGINA     PIC 9(3)      VALUE 99.
           05  WS-MAX-LINHAS           PIC 9(3)      VALUE 10.
           05  WS-PAGINA               PIC 9(4)      VALUE 0.
       01  WS-TOTAIS.
           05  WS-SALDO                PIC S9(13)V99.
           05  WS-TOT-AGENCIA          PIC S9(13)V99 VALUE 0.
           05  WS-QTD-AGENCIA          PIC 9(9)      VALUE 0.
           05  WS-TOT-GERAL            PIC S9(13)V99 VALUE 0.
           05  WS-QTD-GERAL            PIC 9(9)      VALUE 0.
      *---------------------------------------------------------------
      * LINHAS DO RELATORIO (70 POSICOES)
      *---------------------------------------------------------------
       01  WS-CAB1.
           05  FILLER          PIC X(30) VALUE "BANCO VERTICE S.A.".
           05  FILLER          PIC X(29) VALUE "CONTAS DO LITORAL".
           05  FILLER          PIC X(7)  VALUE "PAGINA ".
           05  WS-CAB1-PAGINA  PIC ZZZ9.
       01  WS-CAB2.
           05  FILLER          PIC X(17) VALUE "AGENCIA-CONTA".
           05  FILLER          PIC X(36) VALUE "TITULAR".
           05  FILLER          PIC X(17) VALUE "            SALDO".
       01  WS-DET.
           05  WS-DET-AGENCIA  PIC 9(4).
           05  FILLER          PIC X     VALUE "-".
           05  WS-DET-CONTA    PIC 9(7).
           05  FILLER          PIC X     VALUE "-".
           05  WS-DET-DIGITO   PIC X.
           05  FILLER          PIC X(3)  VALUE SPACES.
           05  WS-DET-NOME     PIC X(22).
           05  FILLER          PIC X(13) VALUE SPACES.
           05  WS-DET-SALDO    PIC ---.---.---.--9,99.
       01  WS-SUB.
           05  FILLER          PIC X(8)  VALUE "  TOTAL ".
           05  WS-SUB-AGENCIA  PIC 9(4).
           05  FILLER          PIC X(3)  VALUE " - ".
           05  WS-SUB-QTD      PIC ZZZ.ZZ9.
           05  FILLER          PIC X(30) VALUE " CONTAS".
           05  WS-SUB-SALDO    PIC ---.---.---.--9,99.
       01  WS-GER.
           05  FILLER          PIC X(15) VALUE "TOTAL GERAL - ".
           05  WS-GER-QTD      PIC ZZZ.ZZ9.
           05  FILLER          PIC X(30) VALUE " CONTAS".
           05  WS-GER-SALDO    PIC ---.---.---.--9,99.
       01  WS-GUARDA-LINHA             PIC X(70).
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM 1000-INICIALIZAR
           PERFORM 2000-PROCESSAR UNTIL FS-LIT-FIM
           PERFORM 3000-FINALIZAR
           GOBACK.
       1000-INICIALIZAR.
           OPEN INPUT ARQ-LITORAL
           IF NOT FS-LIT-OK
               DISPLAY "RELAG01 - OPEN LITCTA STATUS " WS-FS-LITORAL
               PERFORM 9999-ABORTAR
           END-IF
           OPEN OUTPUT ARQ-RELAT
           IF NOT FS-REL-OK
               DISPLAY "RELAG01 - OPEN RELAT STATUS " WS-FS-RELAT
               PERFORM 9999-ABORTAR
           END-IF
           PERFORM 2900-LER
           MOVE LIT-AGENCIA TO WS-AGENCIA-ATUAL.
       2000-PROCESSAR.
           IF LIT-AGENCIA NOT = WS-AGENCIA-ATUAL
               PERFORM 2200-QUEBRA-AGENCIA
           END-IF
           PERFORM 2100-DETALHE
           PERFORM 2900-LER.
       2100-DETALHE.
           IF LIT-SINAL = "-"
               COMPUTE WS-SALDO = LIT-SALDO * -1
           ELSE
               MOVE LIT-SALDO TO WS-SALDO
           END-IF
           ADD WS-SALDO TO WS-TOT-AGENCIA
           ADD 1 TO WS-QTD-AGENCIA
           MOVE LIT-AGENCIA TO WS-DET-AGENCIA
           MOVE LIT-CONTA   TO WS-DET-CONTA
           MOVE LIT-DIGITO  TO WS-DET-DIGITO
           MOVE LIT-NOME    TO WS-DET-NOME
           MOVE WS-SALDO    TO WS-DET-SALDO
           MOVE WS-DET TO REL-LINHA
           PERFORM 2800-IMPRIMIR.
       2200-QUEBRA-AGENCIA.
           MOVE WS-AGENCIA-ATUAL TO WS-SUB-AGENCIA
           MOVE WS-QTD-AGENCIA   TO WS-SUB-QTD
           MOVE WS-TOT-AGENCIA   TO WS-SUB-SALDO
           MOVE WS-SUB TO REL-LINHA
           PERFORM 2800-IMPRIMIR
           MOVE SPACES TO REL-LINHA
           PERFORM 2800-IMPRIMIR
           ADD WS-TOT-AGENCIA TO WS-TOT-GERAL
           ADD WS-QTD-AGENCIA TO WS-QTD-GERAL
           MOVE 0 TO WS-TOT-AGENCIA WS-QTD-AGENCIA
           MOVE LIT-AGENCIA TO WS-AGENCIA-ATUAL.
       2800-IMPRIMIR.
           IF WS-LINHAS-NA-PAGINA >= WS-MAX-LINHAS
               PERFORM 2850-CABECALHO
           END-IF
           WRITE REL-LINHA
           IF NOT FS-REL-OK
               DISPLAY "RELAG01 - WRITE RELAT STATUS " WS-FS-RELAT
               PERFORM 9999-ABORTAR
           END-IF
           ADD 1 TO WS-LINHAS-NA-PAGINA.
       2850-CABECALHO.
           MOVE REL-LINHA TO WS-GUARDA-LINHA
           ADD 1 TO WS-PAGINA
           MOVE WS-PAGINA TO WS-CAB1-PAGINA
           IF WS-PAGINA > 1
               MOVE ALL "=" TO REL-LINHA
               WRITE REL-LINHA
           END-IF
           WRITE REL-LINHA FROM WS-CAB1
           WRITE REL-LINHA FROM WS-CAB2
           MOVE ALL "-" TO REL-LINHA
           WRITE REL-LINHA
           MOVE WS-GUARDA-LINHA TO REL-LINHA
           MOVE 3 TO WS-LINHAS-NA-PAGINA.
       2900-LER.
           READ ARQ-LITORAL
           IF NOT FS-LIT-OK AND NOT FS-LIT-FIM
               DISPLAY "RELAG01 - READ LITCTA STATUS " WS-FS-LITORAL
               PERFORM 9999-ABORTAR
           END-IF.
       3000-FINALIZAR.
           PERFORM 2200-QUEBRA-AGENCIA
           MOVE WS-QTD-GERAL TO WS-GER-QTD
           MOVE WS-TOT-GERAL TO WS-GER-SALDO
           MOVE WS-GER TO REL-LINHA
           PERFORM 2800-IMPRIMIR
           CLOSE ARQ-LITORAL ARQ-RELAT
           DISPLAY "RELAG01 - CONTAS: " WS-QTD-GERAL
                   " PAGINAS: " WS-PAGINA.
       9999-ABORTAR.
           MOVE 12 TO RETURN-CODE
           STOP RUN.
