       IDENTIFICATION DIVISION.
       PROGRAM-ID. DEPARA1.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-DEPARA ASSIGN TO DEPARA
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS-DEPARA.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-DEPARA.
       01  DEP-REGISTRO.
           05  DEP-AG-LITORAL      PIC 9(4).
           05  DEP-NOME            PIC X(20).
           05  DEP-AG-VERTICE      PIC 9(4).
       WORKING-STORAGE SECTION.
       01  WS-FS-DEPARA            PIC XX.
           88  FS-DEP-OK                         VALUE "00".
           88  FS-DEP-FIM                        VALUE "10".
       01  WS-TAB-DEPARA.
           05  WS-QTD-AGENCIAS     PIC 9(4)      VALUE 0.
           05  WS-AGENCIA OCCURS 1 TO 500 TIMES
                   DEPENDING ON WS-QTD-AGENCIAS
                   ASCENDING KEY IS WS-T-AG-LITORAL
                   INDEXED BY IX-AG.
               10  WS-T-AG-LITORAL PIC 9(4).
               10  WS-T-NOME       PIC X(20).
               10  WS-T-AG-VERTICE PIC 9(4).
       01  WS-PROCURADA            PIC 9(4).
       01  WS-NOME-PROCURADO       PIC X(20).
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM 1000-CARREGAR
           MOVE 0205 TO WS-PROCURADA
           PERFORM 2000-PROCURAR
           MOVE 0999 TO WS-PROCURADA
           PERFORM 2000-PROCURAR
           MOVE "SAO VICENTE" TO WS-NOME-PROCURADO
           PERFORM 3000-PROCURAR-NOME
           GOBACK.
       1000-CARREGAR.
           OPEN INPUT ARQ-DEPARA
           IF NOT FS-DEP-OK
               DISPLAY "DEPARA1 - OPEN DEPARA STATUS " WS-FS-DEPARA
               PERFORM 9999-ABORTAR
           END-IF
           READ ARQ-DEPARA
           PERFORM UNTIL NOT FS-DEP-OK
               IF WS-QTD-AGENCIAS = 500
                   DISPLAY "DEPARA1 - TABELA DE AGENCIAS CHEIA"
                   PERFORM 9999-ABORTAR
               END-IF
               ADD 1 TO WS-QTD-AGENCIAS
               MOVE DEP-REGISTRO TO WS-AGENCIA(WS-QTD-AGENCIAS)
               READ ARQ-DEPARA
           END-PERFORM
           IF NOT FS-DEP-FIM
               DISPLAY "DEPARA1 - READ DEPARA STATUS " WS-FS-DEPARA
               PERFORM 9999-ABORTAR
           END-IF
           CLOSE ARQ-DEPARA
           DISPLAY "AGENCIAS CARREGADAS: " WS-QTD-AGENCIAS.
       2000-PROCURAR.
           SEARCH ALL WS-AGENCIA
               AT END
                   DISPLAY WS-PROCURADA " NAO ENCONTRADA"
               WHEN WS-T-AG-LITORAL(IX-AG) = WS-PROCURADA
                   DISPLAY WS-PROCURADA " -> " WS-T-AG-VERTICE(IX-AG)
                           " " WS-T-NOME(IX-AG)
           END-SEARCH.
       3000-PROCURAR-NOME.
           SET IX-AG TO 1
           SEARCH WS-AGENCIA
               AT END
                   DISPLAY WS-NOME-PROCURADO " NAO ENCONTRADA"
               WHEN WS-T-NOME(IX-AG) = WS-NOME-PROCURADO
                   DISPLAY WS-NOME-PROCURADO " E A AGENCIA "
                           WS-T-AG-LITORAL(IX-AG)
           END-SEARCH.
       9999-ABORTAR.
           MOVE 12 TO RETURN-CODE
           STOP RUN.
