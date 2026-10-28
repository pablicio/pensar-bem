       IDENTIFICATION DIVISION.
       PROGRAM-ID. CONVCTA.
      *---------------------------------------------------------------
      * CONVCTA - CONVERSAO DAS CONTAS DO BANCO LITORAL PARA O SICAP
      * ENTRADAS: LITCTA (CONTAS LITORAL, 70 POS., ORDENADO), DEPARA
      * SAIDAS:   VERCTA (CONTAS SICAP, 87 BYTES, COMP-3), REJEIT
      * CONCILIACAO NO FIM: LIDOS = CONVERTIDOS + REJEITADOS +
      * ENCERRADAS, E O MESMO PARA OS SALDOS. SE NAO BATER, RC 12.
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
           DECIMAL-POINT IS COMMA.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-LITORAL ASSIGN TO LITCTA
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-LIT.
           SELECT ARQ-DEPARA ASSIGN TO DEPARA
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-DEP.
           SELECT ARQ-VERTICE ASSIGN TO VERCTA
               ORGANIZATION IS SEQUENTIAL
               FILE STATUS IS WS-FS-VER.
           SELECT ARQ-REJEIT ASSIGN TO REJEIT
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-REJ.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
           COPY LITCTA REPLACING ==:PFX:== BY ==LIT==.
       FD  ARQ-DEPARA.
       01  DEP-REGISTRO.
           05  DEP-AG-LITORAL          PIC 9(4).
           05  DEP-NOME                PIC X(20).
           05  DEP-AG-VERTICE          PIC 9(4).
       FD  ARQ-VERTICE.
           COPY VERCTA.
       FD  ARQ-REJEIT.
       01  REJ-REGISTRO                PIC X(43).
       WORKING-STORAGE SECTION.
       01  WS-REJ-LINHA.
           05  WS-REJ-AGENCIA          PIC 9(4).
           05  FILLER                  PIC X     VALUE "-".
           05  WS-REJ-CONTA            PIC 9(7).
           05  FILLER                  PIC X     VALUE SPACE.
           05  WS-REJ-MOTIVO           PIC X(30).
       01  WS-FS-LIT                   PIC XX.
       01  WS-FS-DEP                   PIC XX.
       01  WS-FS-VER                   PIC XX.
       01  WS-FS-REJ                   PIC XX.
       01  WS-TAB-DEPARA.
           05  WS-QTD-AGENCIAS         PIC 9(4)      VALUE 0.
           05  WS-AGENCIA OCCURS 1 TO 500 TIMES
                   DEPENDING ON WS-QTD-AGENCIAS
                   ASCENDING KEY IS WS-T-AG-LITORAL
                   INDEXED BY IX-AG.
               10  WS-T-AG-LITORAL     PIC 9(4).
               10  WS-T-NOME           PIC X(20).
               10  WS-T-AG-VERTICE     PIC 9(4).
       01  WS-REGISTRO-OK              PIC X.
           88  CND-REGISTRO-OK                   VALUE "S".
       01  WS-MOTIVO                   PIC X(30).
       01  WS-SALDO                    PIC S9(13)V99.
       01  WS-DATA.
           05  WS-ANO                  PIC 9(4).
           05  WS-MES                  PIC 99.
           05  WS-DIA                  PIC 99.
       01  WS-DATA-N REDEFINES WS-DATA PIC 9(8).
       01  WS-DDMMAA.
           05  WS-E-DIA                PIC 99.
           05  WS-E-MES                PIC 99.
           05  WS-E-ANO                PIC 99.
       01  WS-CONTROLE.
           05  WS-QTD-LIDOS            PIC 9(9)      VALUE 0.
           05  WS-QTD-CONVERTIDOS      PIC 9(9)      VALUE 0.
           05  WS-QTD-REJEITADOS       PIC 9(9)      VALUE 0.
           05  WS-QTD-ENCERRADAS       PIC 9(9)      VALUE 0.
           05  WS-QTD-SEM-SALDO        PIC 9(9)      VALUE 0.
           05  WS-SALDO-LIDO           PIC S9(15)V99 VALUE 0.
           05  WS-SALDO-CONVERTIDO     PIC S9(15)V99 VALUE 0.
           05  WS-SALDO-REJEITADO      PIC S9(15)V99 VALUE 0.
           05  WS-SALDO-ENCERRADAS     PIC S9(15)V99 VALUE 0.
       01  WS-ED-QTD                   PIC ZZZ.ZZZ.ZZ9.
       01  WS-ED-SALDO                 PIC -.---.---.---.--9,99.
           COPY VALCPFL.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM 1000-INICIALIZAR
           PERFORM 2000-PROCESSAR UNTIL WS-FS-LIT NOT = "00"
           IF WS-FS-LIT NOT = "10"
               DISPLAY "CONVCTA - READ LITCTA STATUS " WS-FS-LIT
               PERFORM 9999-ABORTAR
           END-IF
           PERFORM 3000-FINALIZAR
           GOBACK.
       1000-INICIALIZAR.
           PERFORM 1100-CARREGAR-DEPARA
           OPEN INPUT ARQ-LITORAL
                OUTPUT ARQ-VERTICE ARQ-REJEIT
           IF WS-FS-LIT NOT = "00" OR WS-FS-VER NOT = "00"
              OR WS-FS-REJ NOT = "00"
               DISPLAY "CONVCTA - OPEN: LITCTA " WS-FS-LIT
                       " VERCTA " WS-FS-VER " REJEIT " WS-FS-REJ
               PERFORM 9999-ABORTAR
           END-IF
           READ ARQ-LITORAL.
       1100-CARREGAR-DEPARA.
           OPEN INPUT ARQ-DEPARA
           IF WS-FS-DEP NOT = "00"
               DISPLAY "CONVCTA - OPEN DEPARA STATUS " WS-FS-DEP
               PERFORM 9999-ABORTAR
           END-IF
           READ ARQ-DEPARA
           PERFORM UNTIL WS-FS-DEP NOT = "00"
               IF WS-QTD-AGENCIAS = 500
                   DISPLAY "CONVCTA - TABELA DE AGENCIAS CHEIA"
                   PERFORM 9999-ABORTAR
               END-IF
               ADD 1 TO WS-QTD-AGENCIAS
               MOVE DEP-REGISTRO TO WS-AGENCIA(WS-QTD-AGENCIAS)
               READ ARQ-DEPARA
           END-PERFORM
           CLOSE ARQ-DEPARA.
       2000-PROCESSAR.
           ADD 1 TO WS-QTD-LIDOS
           MOVE "S" TO WS-REGISTRO-OK
           INITIALIZE VER-REGISTRO
           PERFORM 2100-SALDO
           IF CND-REGISTRO-OK AND LIT-STATUS = "E"
               PERFORM 2900-ENCERRADA
           ELSE
               IF CND-REGISTRO-OK
                   PERFORM 2200-AGENCIA
               END-IF
               IF CND-REGISTRO-OK
                   PERFORM 2300-DOCUMENTO
               END-IF
               IF CND-REGISTRO-OK
                   PERFORM 2400-DATA-ABERTURA
               END-IF
               IF CND-REGISTRO-OK
                   PERFORM 2500-GRAVAR
               ELSE
                   PERFORM 8000-REJEITAR
               END-IF
           END-IF
           READ ARQ-LITORAL.
       2100-SALDO.
           EVALUATE TRUE
               WHEN LIT-SALDO NOT NUMERIC
                   MOVE "SALDO NAO NUMERICO" TO WS-MOTIVO
                   MOVE "N" TO WS-REGISTRO-OK
                   ADD 1 TO WS-QTD-SEM-SALDO
               WHEN LIT-SINAL = "+"
                   MOVE LIT-SALDO TO WS-SALDO
               WHEN LIT-SINAL = "-"
                   COMPUTE WS-SALDO = LIT-SALDO * -1
               WHEN OTHER
                   MOVE "SINAL DO SALDO INVALIDO" TO WS-MOTIVO
                   MOVE "N" TO WS-REGISTRO-OK
                   ADD 1 TO WS-QTD-SEM-SALDO
           END-EVALUATE
           IF CND-REGISTRO-OK
               ADD WS-SALDO TO WS-SALDO-LIDO
           END-IF.
       2200-AGENCIA.
           SEARCH ALL WS-AGENCIA
               AT END
                   MOVE "AGENCIA SEM DE-PARA" TO WS-MOTIVO
                   MOVE "N" TO WS-REGISTRO-OK
               WHEN WS-T-AG-LITORAL(IX-AG) = LIT-AGENCIA
                   MOVE WS-T-AG-VERTICE(IX-AG) TO VER-AGENCIA
           END-SEARCH.
       2300-DOCUMENTO.
           IF LIT-TIPO-PESSOA = "F"
               INITIALIZE LK-VALCPF
               MOVE LIT-DOCUMENTO TO LK-DOCUMENTO
               CALL "VALCPF" USING LK-VALCPF
               IF CND-CPF-VALIDO
                   MOVE LK-CPF-NUMERICO TO VER-CPF-CNPJ
               ELSE
                   STRING "CPF INVALIDO (" LK-RETORNO ")"
                       DELIMITED BY SIZE INTO WS-MOTIVO
                   MOVE "N" TO WS-REGISTRO-OK
               END-IF
           ELSE
               IF LIT-DOCUMENTO IS NUMERIC
                   MOVE LIT-DOCUMENTO TO VER-CPF-CNPJ
               ELSE
                   MOVE "CNPJ INVALIDO" TO WS-MOTIVO
                   MOVE "N" TO WS-REGISTRO-OK
               END-IF
           END-IF.
       2400-DATA-ABERTURA.
      *    JANELA: AA >= 72 -> 19AA. EM BRANCO -> 01/01/1994, COM
      *    OBSERVACAO "D" (DECISAO DA REDE DE AGENCIAS, 14/01/2027).
           EVALUATE TRUE
               WHEN LIT-DATA-ABERTURA = SPACES
                   MOVE 19940101 TO VER-DT-ABERTURA
                   MOVE "D" TO VER-OBS(1:1)
               WHEN LIT-DATA-ABERTURA NOT NUMERIC
                   MOVE "DATA DE ABERTURA INVALIDA" TO WS-MOTIVO
                   MOVE "N" TO WS-REGISTRO-OK
               WHEN OTHER
                   MOVE LIT-DATA-ABERTURA TO WS-DDMMAA
                   IF WS-E-ANO >= 72
                       COMPUTE WS-ANO = 1900 + WS-E-ANO
                   ELSE
                       COMPUTE WS-ANO = 2000 + WS-E-ANO
                   END-IF
                   MOVE WS-E-MES TO WS-MES
                   MOVE WS-E-DIA TO WS-DIA
                   IF FUNCTION TEST-DATE-YYYYMMDD(WS-DATA-N) = 0
                       MOVE WS-DATA-N TO VER-DT-ABERTURA
                   ELSE
                       MOVE "DATA DE ABERTURA NAO EXISTE" TO WS-MOTIVO
                       MOVE "N" TO WS-REGISTRO-OK
                   END-IF
           END-EVALUATE.
       2500-GRAVAR.
           MOVE LIT-CONTA       TO VER-CONTA
           MOVE LIT-DIGITO      TO VER-DIGITO
           MOVE LIT-NOME        TO VER-NOME
           MOVE LIT-TIPO-PESSOA TO VER-TIPO-PESSOA
           MOVE WS-SALDO        TO VER-SALDO
           MOVE LIT-STATUS      TO VER-SITUACAO
           MOVE "LIT"           TO VER-ORIGEM
           MOVE LIT-AGENCIA     TO VER-AG-ORIGEM
           IF LIT-NOME(22:1) NOT = SPACE
               MOVE "N" TO VER-OBS(2:1)
           END-IF
           WRITE VER-REGISTRO
           IF WS-FS-VER NOT = "00"
               DISPLAY "CONVCTA - WRITE VERCTA STATUS " WS-FS-VER
               PERFORM 9999-ABORTAR
           END-IF
           ADD 1 TO WS-QTD-CONVERTIDOS
           ADD WS-SALDO TO WS-SALDO-CONVERTIDO.
       2900-ENCERRADA.
           ADD 1 TO WS-QTD-ENCERRADAS
           ADD WS-SALDO TO WS-SALDO-ENCERRADAS.
       8000-REJEITAR.
           ADD 1 TO WS-QTD-REJEITADOS
           IF WS-MOTIVO NOT = "SALDO NAO NUMERICO"
              AND WS-MOTIVO NOT = "SINAL DO SALDO INVALIDO"
               ADD WS-SALDO TO WS-SALDO-REJEITADO
           END-IF
           MOVE LIT-AGENCIA TO WS-REJ-AGENCIA
           MOVE LIT-CONTA   TO WS-REJ-CONTA
           MOVE WS-MOTIVO   TO WS-REJ-MOTIVO
           WRITE REJ-REGISTRO FROM WS-REJ-LINHA
           MOVE SPACES TO WS-MOTIVO.
       3000-FINALIZAR.
           CLOSE ARQ-LITORAL ARQ-VERTICE ARQ-REJEIT
           DISPLAY "CONVCTA - CONCILIACAO"
           MOVE WS-QTD-LIDOS TO WS-ED-QTD
           DISPLAY "  LIDOS ............ " WS-ED-QTD
           MOVE WS-QTD-CONVERTIDOS TO WS-ED-QTD
           DISPLAY "  CONVERTIDOS ...... " WS-ED-QTD
           MOVE WS-QTD-REJEITADOS TO WS-ED-QTD
           DISPLAY "  REJEITADOS ....... " WS-ED-QTD
           MOVE WS-QTD-ENCERRADAS TO WS-ED-QTD
           DISPLAY "  ENCERRADAS ....... " WS-ED-QTD
           MOVE WS-SALDO-LIDO TO WS-ED-SALDO
           DISPLAY "  SALDO LIDO ....... " WS-ED-SALDO
           MOVE WS-SALDO-CONVERTIDO TO WS-ED-SALDO
           DISPLAY "  SALDO CONVERTIDO . " WS-ED-SALDO
           MOVE WS-SALDO-REJEITADO TO WS-ED-SALDO
           DISPLAY "  SALDO REJEITADO .. " WS-ED-SALDO
           IF WS-QTD-LIDOS NOT = WS-QTD-CONVERTIDOS
                  + WS-QTD-REJEITADOS + WS-QTD-ENCERRADAS
              OR WS-SALDO-LIDO NOT = WS-SALDO-CONVERTIDO
                  + WS-SALDO-REJEITADO + WS-SALDO-ENCERRADAS
               DISPLAY "CONVCTA - CONCILIACAO NAO FECHA"
               MOVE 12 TO RETURN-CODE
           ELSE
               DISPLAY "CONVCTA - CONCILIACAO FECHADA"
               IF WS-QTD-REJEITADOS > 0
                   MOVE 4 TO RETURN-CODE
               END-IF
           END-IF.
       9999-ABORTAR.
           MOVE 12 TO RETURN-CODE
           STOP RUN.
