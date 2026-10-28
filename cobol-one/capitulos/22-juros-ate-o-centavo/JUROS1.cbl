       IDENTIFICATION DIVISION.
       PROGRAM-ID. JUROS1.
      *---------------------------------------------------------------
      * JUROS DE CHEQUE ESPECIAL SOBRE O SALDO DEVEDOR DIARIO
      * TAXA DIARIA = TAXA MENSAL / 30 (JUROS SIMPLES NO MES).
      * PF: TAXA LIMITADA A 8% AM (RESOLUCAO CMN 4.765/2019,
      * VIGENCIA 06/01/2020).
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
           05  SAL-DATA                PIC 9(8).
           05  SAL-SALDO               PIC S9(9)V99
                                       SIGN IS LEADING SEPARATE.
       WORKING-STORAGE SECTION.
       01  WS-FS                       PIC XX.
       01  WS-TIPO-PESSOA              PIC X     VALUE "F".
       01  WS-TAXA-CONTRATO            PIC S9V9(9) VALUE 0,092.
       01  WS-TETO-PF                  PIC S9V9(9) VALUE 0,08.
       01  WS-TAXA-APLICADA            PIC S9V9(9).
       01  WS-SALDO-DEVEDOR            PIC S9(9)V99.
       01  WS-JUROS-DIA                PIC S9(9)V9(8).
       01  WS-JUROS-ACUM               PIC S9(9)V9(8) VALUE 0.
       01  WS-JUROS-COBRAR             PIC S9(9)V99.
       01  WS-DIAS-DEVEDOR             PIC 99    VALUE 0.
       01  WS-ED-VALOR                 PIC --.---.--9,99.
       01  WS-ED-JUROS                 PIC -9,99999999.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM 1000-DEFINIR-TAXA
           OPEN INPUT ARQ-SALDOS
           IF WS-FS NOT = "00"
               DISPLAY "JUROS1 - OPEN SALDOS STATUS " WS-FS
               MOVE 12 TO RETURN-CODE
               GOBACK
           END-IF
           READ ARQ-SALDOS
           PERFORM UNTIL WS-FS NOT = "00"
               IF SAL-SALDO < 0
                   PERFORM 2000-JUROS-DO-DIA
               END-IF
               READ ARQ-SALDOS
           END-PERFORM
           CLOSE ARQ-SALDOS
           COMPUTE WS-JUROS-COBRAR ROUNDED = WS-JUROS-ACUM
           MOVE WS-JUROS-COBRAR TO WS-ED-VALOR
           DISPLAY "DIAS DEVEDORES: " WS-DIAS-DEVEDOR
                   "  JUROS A COBRAR: " WS-ED-VALOR
           GOBACK.
       1000-DEFINIR-TAXA.
           MOVE WS-TAXA-CONTRATO TO WS-TAXA-APLICADA
           IF WS-TIPO-PESSOA = "F"
              AND WS-TAXA-CONTRATO > WS-TETO-PF
               MOVE WS-TETO-PF TO WS-TAXA-APLICADA
               DISPLAY "TAXA DO CONTRATO ACIMA DO TETO: APLICADO 8%"
           END-IF.
       2000-JUROS-DO-DIA.
           ADD 1 TO WS-DIAS-DEVEDOR
           COMPUTE WS-SALDO-DEVEDOR = SAL-SALDO * -1
           COMPUTE WS-JUROS-DIA =
                   WS-SALDO-DEVEDOR * WS-TAXA-APLICADA / 30
           ADD WS-JUROS-DIA TO WS-JUROS-ACUM
           MOVE SAL-SALDO TO WS-ED-VALOR
           MOVE WS-JUROS-DIA TO WS-ED-JUROS
           DISPLAY SAL-DATA " SALDO " WS-ED-VALOR
                   "  JUROS DO DIA " WS-ED-JUROS.
