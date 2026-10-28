       IDENTIFICATION DIVISION.
       PROGRAM-ID. COMP3A.
      *---------------------------------------------------------------
      * MOSTRA COMO OS FORMATOS NUMERICOS FICAM NOS BYTES
      *---------------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-EXIB                 PIC S9(5)V99  VALUE -123.45.
       01  WS-EXIB-X REDEFINES WS-EXIB          PIC X(7).
       01  WS-PACK-NEG             PIC S9(5)V99  COMP-3 VALUE -123.45.
       01  WS-PACK-NEG-X REDEFINES WS-PACK-NEG  PIC X(4).
       01  WS-PACK-POS             PIC S9(5)V99  COMP-3 VALUE 123.45.
       01  WS-PACK-POS-X REDEFINES WS-PACK-POS  PIC X(4).
       01  WS-PACK-SEM             PIC 9(5)V99   COMP-3 VALUE 123.45.
       01  WS-PACK-SEM-X REDEFINES WS-PACK-SEM  PIC X(4).
       01  WS-BIN                  PIC S9(4)     COMP   VALUE 1234.
       01  WS-BIN-X REDEFINES WS-BIN            PIC X(2).
       01  WS-SALDO-SICAP          PIC S9(13)V99 COMP-3.
      *    AREA DO DUMP HEXADECIMAL
       01  WS-AREA                 PIC X(10).
       01  WS-TAM                  PIC 99.
       01  WS-HEX                  PIC X(20).
       01  WS-I                    PIC 99.
       01  WS-BYTE                 PIC 999.
       01  WS-DIGITOS-HEX          PIC X(16) VALUE "0123456789ABCDEF".
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           DISPLAY "BYTES: EXIBICAO " LENGTH OF WS-EXIB
                   " COMP-3 " LENGTH OF WS-PACK-NEG
                   " COMP " LENGTH OF WS-BIN
                   " SALDO SICAP " LENGTH OF WS-SALDO-SICAP
           MOVE WS-PACK-POS-X TO WS-AREA
           MOVE 4 TO WS-TAM
           PERFORM 9000-HEX
           DISPLAY "COMP-3  +123,45: " WS-HEX
           MOVE WS-PACK-NEG-X TO WS-AREA
           PERFORM 9000-HEX
           DISPLAY "COMP-3  -123,45: " WS-HEX
           MOVE WS-PACK-SEM-X TO WS-AREA
           PERFORM 9000-HEX
           DISPLAY "SEM SINAL 123,45: " WS-HEX
           MOVE WS-BIN-X TO WS-AREA
           MOVE 2 TO WS-TAM
           PERFORM 9000-HEX
           DISPLAY "COMP    1234:    " WS-HEX
           MOVE WS-EXIB-X TO WS-AREA
           MOVE 7 TO WS-TAM
           PERFORM 9000-HEX
           DISPLAY "EXIBICAO -123,45: " WS-HEX
           GOBACK.
      *---------------------------------------------------------------
      * ESCREVE EM WS-HEX OS WS-TAM PRIMEIROS BYTES DE WS-AREA
      *---------------------------------------------------------------
       9000-HEX.
           MOVE SPACES TO WS-HEX
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > WS-TAM
               COMPUTE WS-BYTE = FUNCTION ORD(WS-AREA(WS-I:1)) - 1
               MOVE WS-DIGITOS-HEX(WS-BYTE / 16 + 1:1)
                   TO WS-HEX(WS-I * 2 - 1:1)
               MOVE WS-DIGITOS-HEX(FUNCTION MOD(WS-BYTE, 16) + 1:1)
                   TO WS-HEX(WS-I * 2:1)
           END-PERFORM.
