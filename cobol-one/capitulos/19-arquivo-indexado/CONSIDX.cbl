       IDENTIFICATION DIVISION.
       PROGRAM-ID. CONSIDX.
      *---------------------------------------------------------------
      * CONSULTAS AO ARQUIVO INDEXADO DE CONTAS DO LITORAL
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-CONTAS ASSIGN TO CONTAS
               ORGANIZATION IS INDEXED
               ACCESS MODE IS DYNAMIC
               RECORD KEY IS IDX-CHAVE
               ALTERNATE RECORD KEY IS IDX-DOCUMENTO WITH DUPLICATES
               FILE STATUS IS WS-FS-IDX.
       DATA DIVISION.
       FILE SECTION.
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
       01  WS-FS-IDX                   PIC XX.
           88  FS-IDX-OK                         VALUE "00" "02".
           88  FS-IDX-NAO-ACHOU                  VALUE "23".
           88  FS-IDX-FIM                        VALUE "10".
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           OPEN I-O ARQ-CONTAS
           IF NOT FS-IDX-OK
               DISPLAY "CONSIDX - OPEN CONTAS STATUS " WS-FS-IDX
               MOVE 12 TO RETURN-CODE
               GOBACK
           END-IF
           MOVE 0205 TO IDX-AGENCIA
           MOVE 0040027 TO IDX-CONTA
           PERFORM 1000-LER-POR-CONTA
           MOVE 0999 TO IDX-AGENCIA
           MOVE 0000001 TO IDX-CONTA
           PERFORM 1000-LER-POR-CONTA
           PERFORM 2000-LISTAR-AGENCIA-0102
           PERFORM 3000-LER-POR-DOCUMENTO
           PERFORM 4000-ALTERAR-E-APAGAR
           CLOSE ARQ-CONTAS
           GOBACK.
       1000-LER-POR-CONTA.
           READ ARQ-CONTAS
               KEY IS IDX-CHAVE
               INVALID KEY
                   DISPLAY "CONTA " IDX-AGENCIA "-" IDX-CONTA
                           " NAO ENCONTRADA (STATUS " WS-FS-IDX ")"
               NOT INVALID KEY
                   DISPLAY "CONTA " IDX-AGENCIA "-" IDX-CONTA ": "
                           IDX-NOME
           END-READ.
       2000-LISTAR-AGENCIA-0102.
           DISPLAY "CONTAS DA AGENCIA 0102:"
           MOVE 0102 TO IDX-AGENCIA
           MOVE 0 TO IDX-CONTA
           START ARQ-CONTAS KEY IS >= IDX-CHAVE
               INVALID KEY
                   DISPLAY "  NENHUMA"
           END-START
           PERFORM UNTIL NOT FS-IDX-OK
               READ ARQ-CONTAS NEXT RECORD
                   AT END
                       CONTINUE
                   NOT AT END
                       IF IDX-AGENCIA = 0102
                           DISPLAY "  " IDX-CONTA " " IDX-NOME
                       ELSE
                           MOVE "10" TO WS-FS-IDX
                       END-IF
               END-READ
           END-PERFORM.
       3000-LER-POR-DOCUMENTO.
           MOVE "999.888.777-14" TO IDX-DOCUMENTO
           READ ARQ-CONTAS
               KEY IS IDX-DOCUMENTO
               INVALID KEY
                   DISPLAY "DOCUMENTO NAO ENCONTRADO"
               NOT INVALID KEY
                   DISPLAY "DOCUMENTO " IDX-DOCUMENTO ": "
                           IDX-AGENCIA "-" IDX-CONTA " " IDX-NOME
           END-READ.
       4000-ALTERAR-E-APAGAR.
           MOVE 0101 TO IDX-AGENCIA
           MOVE 0012353 TO IDX-CONTA
           READ ARQ-CONTAS KEY IS IDX-CHAVE
           MOVE "JOSE CARLOS PEREIRA FO" TO IDX-NOME
           REWRITE IDX-REGISTRO
               INVALID KEY
                   DISPLAY "REWRITE FALHOU " WS-FS-IDX
           END-REWRITE
           PERFORM 1000-LER-POR-CONTA
           MOVE 0102 TO IDX-AGENCIA
           MOVE 0030077 TO IDX-CONTA
           DELETE ARQ-CONTAS RECORD
               INVALID KEY
                   DISPLAY "DELETE FALHOU " WS-FS-IDX
           END-DELETE
           PERFORM 1000-LER-POR-CONTA.
