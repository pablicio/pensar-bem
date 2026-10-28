       IDENTIFICATION DIVISION.
       PROGRAM-ID. IDCONTA.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-AGENCIA              PIC 9(4)      VALUE 0101.
       01  WS-CONTA                PIC 9(7)      VALUE 12345.
       01  WS-DIGITO               PIC X         VALUE "7".
       01  WS-ID                   PIC X(14).
       PROCEDURE DIVISION.
           MOVE SPACES TO WS-ID
           STRING WS-AGENCIA DELIMITED BY SIZE
                  "."        DELIMITED BY SIZE
                  WS-CONTA   DELIMITED BY SIZE
                  "-"        DELIMITED BY SIZE
                  WS-DIGITO  DELIMITED BY SIZE
               INTO WS-ID
           END-STRING
           DISPLAY WS-ID
           GOBACK.
