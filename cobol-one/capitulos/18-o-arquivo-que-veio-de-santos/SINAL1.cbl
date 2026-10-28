       IDENTIFICATION DIVISION.
       PROGRAM-ID. SINAL1.
      *---------------------------------------------------------------
      * LE SALDOS COM SINAL EMBUTIDO NO ULTIMO DIGITO (MAINFRAME)
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
           DECIMAL-POINT IS COMMA.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-SALDOS ASSIGN TO SALDOS
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FS.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-SALDOS.
       01  SAL-REGISTRO.
           05  SAL-AGENCIA             PIC 9(4).
           05  SAL-CONTA               PIC 9(7).
           05  SAL-SALDO               PIC S9(11)V99.
           05  SAL-SALDO-X REDEFINES SAL-SALDO PIC X(13).
       WORKING-STORAGE SECTION.
       01  WS-FS                       PIC XX.
       01  WS-ED-SALDO                 PIC -.---.---.--9,99.
       PROCEDURE DIVISION.
           OPEN INPUT ARQ-SALDOS
           IF WS-FS NOT = "00"
               DISPLAY "SINAL1 - OPEN SALDOS STATUS " WS-FS
               MOVE 12 TO RETURN-CODE
               GOBACK
           END-IF
           READ ARQ-SALDOS
           PERFORM UNTIL WS-FS NOT = "00"
               IF SAL-SALDO NUMERIC
                   MOVE SAL-SALDO TO WS-ED-SALDO
                   DISPLAY SAL-AGENCIA "-" SAL-CONTA " " WS-ED-SALDO
               ELSE
                   DISPLAY SAL-AGENCIA "-" SAL-CONTA
                           " SALDO INVALIDO: [" SAL-SALDO-X "]"
               END-IF
               READ ARQ-SALDOS
           END-PERFORM
           CLOSE ARQ-SALDOS
           GOBACK.
