       IDENTIFICATION DIVISION.
       PROGRAM-ID. ABREV1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-COD              PIC 9         VALUE 1.
       PROCEDURE DIVISION.
           IF WS-COD NOT = 1 OR 2
               DISPLAY "CODIGO NAO E 1 NEM 2?"
           ELSE
               DISPLAY "CODIGO E 1 OU 2"
           END-IF
           GOBACK.
