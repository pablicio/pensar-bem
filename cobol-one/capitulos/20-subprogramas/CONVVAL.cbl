       IDENTIFICATION DIVISION.
       PROGRAM-ID. CONVVAL.
      *---------------------------------------------------------------
      * VALIDA OS DOCUMENTOS DAS CONTAS DO LITORAL (PESSOA FISICA)
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-LITORAL ASSIGN TO LITCTA
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-LIT.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
           COPY LITCTA REPLACING ==:PFX:== BY ==LIT==.
       WORKING-STORAGE SECTION.
       01  WS-FS-LIT                   PIC XX.
       01  WS-QTD-VALIDOS              PIC 9(9)  VALUE 0.
       01  WS-QTD-INVALIDOS            PIC 9(9)  VALUE 0.
           COPY VALCPFL.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           OPEN INPUT ARQ-LITORAL
           IF WS-FS-LIT NOT = "00"
               DISPLAY "CONVVAL - OPEN LITCTA STATUS " WS-FS-LIT
               MOVE 12 TO RETURN-CODE
               GOBACK
           END-IF
           READ ARQ-LITORAL
           PERFORM UNTIL WS-FS-LIT NOT = "00"
               IF LIT-TIPO-PESSOA = "F"
                   PERFORM 1000-VALIDAR
               END-IF
               READ ARQ-LITORAL
           END-PERFORM
           CLOSE ARQ-LITORAL
           DISPLAY "VALIDOS: " WS-QTD-VALIDOS
                   " INVALIDOS: " WS-QTD-INVALIDOS
           GOBACK.
       1000-VALIDAR.
           INITIALIZE LK-VALCPF
           MOVE LIT-DOCUMENTO TO LK-DOCUMENTO
           CALL "VALCPF" USING LK-VALCPF
           IF CND-CPF-VALIDO
               ADD 1 TO WS-QTD-VALIDOS
           ELSE
               ADD 1 TO WS-QTD-INVALIDOS
               DISPLAY "CPF INVALIDO (" LK-RETORNO "): "
                       LIT-AGENCIA "-" LIT-CONTA " " LIT-DOCUMENTO
           END-IF.
