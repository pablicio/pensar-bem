       IDENTIFICATION DIVISION.
       PROGRAM-ID. CRIAIDX.
      *---------------------------------------------------------------
      * CARREGA AS CONTAS DO LITORAL NUM ARQUIVO INDEXADO
      * CHAVE PRIMARIA: AGENCIA + CONTA. ALTERNATIVA: DOCUMENTO.
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-LITORAL ASSIGN TO LITCTA
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-LIT.
           SELECT ARQ-CONTAS ASSIGN TO CONTAS
               ORGANIZATION IS INDEXED
               ACCESS MODE IS DYNAMIC
               RECORD KEY IS IDX-CHAVE
               ALTERNATE RECORD KEY IS IDX-DOCUMENTO WITH DUPLICATES
               FILE STATUS IS WS-FS-IDX.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-LITORAL.
           COPY LITCTA REPLACING ==:PFX:== BY ==LIT==.
       FD  ARQ-CONTAS.
       01  IDX-REGISTRO.
           05  IDX-CHAVE.
               10  IDX-AGENCIA         PIC 9(4).
               10  IDX-CONTA           PIC 9(7).
           05  IDX-DIGITO              PIC X.
           05  IDX-NOME                PIC X(22).
           05  IDX-DOCUMENTO           PIC X(14).
           05  IDX-RESTO               PIC X(22).
       WORKING-STORAGE SECTION.
       01  WS-FS-LIT                   PIC XX.
       01  WS-FS-IDX                   PIC XX.
       01  WS-GRAVADOS                 PIC 9(9)  VALUE 0.
       01  WS-DUPLICADOS               PIC 9(9)  VALUE 0.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           OPEN INPUT ARQ-LITORAL
           OPEN OUTPUT ARQ-CONTAS
           IF WS-FS-LIT NOT = "00" OR WS-FS-IDX NOT = "00"
               DISPLAY "CRIAIDX - OPEN: LITCTA " WS-FS-LIT
                       " CONTAS " WS-FS-IDX
               MOVE 12 TO RETURN-CODE
               GOBACK
           END-IF
           READ ARQ-LITORAL
           PERFORM UNTIL WS-FS-LIT NOT = "00"
               MOVE LIT-REGISTRO TO IDX-REGISTRO
               WRITE IDX-REGISTRO
                   INVALID KEY
                       ADD 1 TO WS-DUPLICADOS
                       DISPLAY "CHAVE DUPLICADA: " IDX-CHAVE
                               " STATUS " WS-FS-IDX
                   NOT INVALID KEY
                       ADD 1 TO WS-GRAVADOS
               END-WRITE
               READ ARQ-LITORAL
           END-PERFORM
           CLOSE ARQ-LITORAL ARQ-CONTAS
           DISPLAY "CRIAIDX - GRAVADOS: " WS-GRAVADOS
                   " DUPLICADOS: " WS-DUPLICADOS
           GOBACK.
