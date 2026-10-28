       IDENTIFICATION DIVISION.
       PROGRAM-ID. STRING1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-AGENCIA              PIC X(4)      VALUE "0101".
       01  WS-NOME                 PIC X(20) VALUE "SANTOS CENTRO".
       01  WS-UF                   PIC X(2)      VALUE "SP".
       01  WS-SAIDA                PIC X(30).
       01  WS-PONTEIRO             PIC 99.
       PROCEDURE DIVISION.
           MOVE SPACES TO WS-SAIDA
           MOVE 1 TO WS-PONTEIRO
           STRING WS-AGENCIA DELIMITED BY SIZE
                  " - "      DELIMITED BY SIZE
                  WS-NOME    DELIMITED BY "  "
                  "/"        DELIMITED BY SIZE
                  WS-UF      DELIMITED BY SIZE
               INTO WS-SAIDA WITH POINTER WS-PONTEIRO
               ON OVERFLOW
                   DISPLAY "NAO COUBE"
           END-STRING
           DISPLAY "[" WS-SAIDA "] PROXIMA POSICAO: " WS-PONTEIRO
           GOBACK.
