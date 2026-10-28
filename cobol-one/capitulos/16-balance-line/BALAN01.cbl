       IDENTIFICATION DIVISION.
       PROGRAM-ID. BALAN01.
      *---------------------------------------------------------------
      * BALANCE LINE: CLIENTES DO LITORAL X CADASTRO DO VERTICE
      * ENTRADAS ORDENADAS POR CPF. VERCLI TEM UM REGISTRO POR CPF.
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-LITORAL ASSIGN TO LITCLI
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-LIT.
           SELECT ARQ-VERTICE ASSIGN TO VERCLI
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-VER.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
       01  LIT-REGISTRO.
           05  LIT-CPF                 PIC X(11).
           05  LIT-NOME                PIC X(22).
           05  LIT-AGENCIA             PIC 9(4).
           05  LIT-CONTA               PIC 9(7).
       FD  ARQ-VERTICE.
       01  VER-REGISTRO.
           05  VER-CPF                 PIC X(11).
           05  VER-CODIGO              PIC 9(9).
           05  VER-NOME                PIC X(30).
       WORKING-STORAGE SECTION.
       01  WS-FS-LIT                   PIC XX.
           88  FS-LIT-OK                         VALUE "00".
       01  WS-FS-VER                   PIC XX.
           88  FS-VER-OK                         VALUE "00".
       01  WS-CHAVE-LIT                PIC X(11).
       01  WS-CHAVE-VER                PIC X(11).
       01  WS-ULTIMO-NOVO              PIC X(11) VALUE SPACES.
       01  WS-CONTADORES.
           05  WS-QTD-EXISTENTES       PIC 9(9)  VALUE 0.
           05  WS-QTD-NOVOS            PIC 9(9)  VALUE 0.
           05  WS-QTD-CONTAS           PIC 9(9)  VALUE 0.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM 1000-INICIALIZAR
           PERFORM 2000-CASAR
               UNTIL WS-CHAVE-LIT = HIGH-VALUES
                 AND WS-CHAVE-VER = HIGH-VALUES
           PERFORM 3000-FINALIZAR
           GOBACK.
       1000-INICIALIZAR.
           OPEN INPUT ARQ-LITORAL ARQ-VERTICE
           IF NOT FS-LIT-OK OR NOT FS-VER-OK
               DISPLAY "BALAN01 - ERRO NO OPEN: LITCLI " WS-FS-LIT
                       " VERCLI " WS-FS-VER
               MOVE 12 TO RETURN-CODE
               STOP RUN
           END-IF
           PERFORM 2100-LER-LITORAL
           PERFORM 2200-LER-VERTICE.
       2000-CASAR.
           EVALUATE TRUE
               WHEN WS-CHAVE-LIT = WS-CHAVE-VER
                   PERFORM 2300-JA-E-CLIENTE
                   PERFORM 2100-LER-LITORAL
               WHEN WS-CHAVE-LIT < WS-CHAVE-VER
                   PERFORM 2400-CLIENTE-NOVO
                   PERFORM 2100-LER-LITORAL
               WHEN OTHER
                   PERFORM 2200-LER-VERTICE
           END-EVALUATE.
       2100-LER-LITORAL.
           READ ARQ-LITORAL
           EVALUATE WS-FS-LIT
               WHEN "00"
                   MOVE LIT-CPF TO WS-CHAVE-LIT
                   ADD 1 TO WS-QTD-CONTAS
               WHEN "10"
                   MOVE HIGH-VALUES TO WS-CHAVE-LIT
               WHEN OTHER
                   DISPLAY "BALAN01 - READ LITCLI STATUS " WS-FS-LIT
                   MOVE 12 TO RETURN-CODE
                   STOP RUN
           END-EVALUATE.
       2200-LER-VERTICE.
           READ ARQ-VERTICE
           EVALUATE WS-FS-VER
               WHEN "00"
                   MOVE VER-CPF TO WS-CHAVE-VER
               WHEN "10"
                   MOVE HIGH-VALUES TO WS-CHAVE-VER
               WHEN OTHER
                   DISPLAY "BALAN01 - READ VERCLI STATUS " WS-FS-VER
                   MOVE 12 TO RETURN-CODE
                   STOP RUN
           END-EVALUATE.
       2300-JA-E-CLIENTE.
           ADD 1 TO WS-QTD-EXISTENTES
           DISPLAY "EXISTE  " LIT-CPF " " LIT-AGENCIA "-" LIT-CONTA
                   " -> CLIENTE " VER-CODIGO
           IF LIT-NOME NOT = VER-NOME(1:22)
               DISPLAY "        NOME DIFERENTE: " VER-NOME
           END-IF.
       2400-CLIENTE-NOVO.
           IF LIT-CPF = WS-ULTIMO-NOVO
               DISPLAY "NOVO    " LIT-CPF " " LIT-AGENCIA "-"
                       LIT-CONTA " (MESMO CLIENTE DA LINHA ANTERIOR)"
           ELSE
               ADD 1 TO WS-QTD-NOVOS
               MOVE LIT-CPF TO WS-ULTIMO-NOVO
               DISPLAY "NOVO    " LIT-CPF " " LIT-AGENCIA "-"
                       LIT-CONTA
           END-IF.
       3000-FINALIZAR.
           CLOSE ARQ-LITORAL ARQ-VERTICE
           DISPLAY "CONTAS DO LITORAL:        " WS-QTD-CONTAS
           DISPLAY "CONTAS DE QUEM JA E CLIENTE: " WS-QTD-EXISTENTES
           DISPLAY "CLIENTES NOVOS:           " WS-QTD-NOVOS.
