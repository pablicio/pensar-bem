       IDENTIFICATION DIVISION.
       PROGRAM-ID. GRUPO1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-CONTA.
           05  WS-AGENCIA      PIC 9(4).
           05  WS-NUMERO       PIC 9(8).
       PROCEDURE DIVISION.
           MOVE 5 TO WS-CONTA
           DISPLAY "CONTA:   [" WS-CONTA "]"
           DISPLAY "AGENCIA: [" WS-AGENCIA "]"
           INITIALIZE WS-CONTA
           DISPLAY "CONTA:   [" WS-CONTA "]"
           GOBACK.
