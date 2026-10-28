       IDENTIFICATION DIVISION.
       PROGRAM-ID. FSTAT1.
      *---------------------------------------------------------------
      * LE O ARQUIVO DO LITORAL CONFERINDO O FILE STATUS
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-LITORAL ASSIGN TO LITCTA
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-LITORAL.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
       01  LIT-REGISTRO.
           05  LIT-DADOS           PIC X(70).
           05  LIT-EXCESSO         PIC X(10).
       WORKING-STORAGE SECTION.
       01  WS-FS-LITORAL           PIC XX.
           88  FS-LIT-OK                         VALUE "00".
           88  FS-LIT-FIM                        VALUE "10".
       01  WS-LIDOS                PIC 9(9)      VALUE 0.
       01  WS-OPERACAO             PIC X(10).
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM 1000-INICIALIZAR
           PERFORM 2000-PROCESSAR UNTIL FS-LIT-FIM
           PERFORM 3000-FINALIZAR
           GOBACK.
       1000-INICIALIZAR.
           MOVE "OPEN" TO WS-OPERACAO
           OPEN INPUT ARQ-LITORAL
           IF NOT FS-LIT-OK
               PERFORM 9999-ABORTAR
           END-IF
           PERFORM 2100-LER.
       2000-PROCESSAR.
           ADD 1 TO WS-LIDOS
           IF LIT-EXCESSO NOT = SPACES
               DISPLAY "FSTAT1 - REGISTRO " WS-LIDOS
                       " TEM MAIS DE 70 POSICOES"
               MOVE "TAMANHO" TO WS-OPERACAO
               PERFORM 9999-ABORTAR
           END-IF
           PERFORM 2100-LER.
       2100-LER.
           MOVE "READ" TO WS-OPERACAO
           READ ARQ-LITORAL
           IF NOT FS-LIT-OK AND NOT FS-LIT-FIM
               PERFORM 9999-ABORTAR
           END-IF.
       3000-FINALIZAR.
           MOVE "CLOSE" TO WS-OPERACAO
           CLOSE ARQ-LITORAL
           IF NOT FS-LIT-OK
               PERFORM 9999-ABORTAR
           END-IF
           DISPLAY "FSTAT1 - REGISTROS LIDOS: " WS-LIDOS.
       9999-ABORTAR.
           DISPLAY "FSTAT1 - ERRO NO ARQUIVO LITCTA"
           DISPLAY "FSTAT1 - OPERACAO: " WS-OPERACAO
                   " FILE STATUS: " WS-FS-LITORAL
      *    FECHA SE ESTIVER ABERTO; AQUI O STATUS NAO IMPORTA
           CLOSE ARQ-LITORAL
           MOVE 12 TO RETURN-CODE
           GOBACK.
