       IDENTIFICATION DIVISION.
       PROGRAM-ID. LOOP1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-FIM                  PIC X         VALUE "N".
       01  WS-VOLTAS               PIC 9(18)     VALUE 0.
       PROCEDURE DIVISION.
           PERFORM UNTIL WS-FIM = "S"
               ADD 1 TO WS-VOLTAS
           END-PERFORM
           DISPLAY "NUNCA CHEGA AQUI"
           GOBACK.
