       IDENTIFICATION DIVISION.
       PROGRAM-ID. NIVEL88.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-STATUS-CONTA     PIC X         VALUE "J".
           88  CND-ATIVA                     VALUE "A".
           88  CND-BLOQUEADA                 VALUE "B" "J".
           88  CND-ENCERRADA                 VALUE "E".
           88  CND-STATUS-VALIDO             VALUE "A" "B" "J" "E".
       01  WS-CODIGO           PIC 99        VALUE 7.
           88  CND-CODIGO-PF                 VALUE 1 THRU 9.
       PROCEDURE DIVISION.
           IF CND-BLOQUEADA
               DISPLAY "CONTA BLOQUEADA: " WS-STATUS-CONTA
           END-IF
           IF CND-CODIGO-PF
               DISPLAY "PESSOA FISICA"
           END-IF
           SET CND-ATIVA TO TRUE
           DISPLAY "STATUS AGORA: " WS-STATUS-CONTA
           MOVE "X" TO WS-STATUS-CONTA
           IF NOT CND-STATUS-VALIDO
               DISPLAY "STATUS INVALIDO: " WS-STATUS-CONTA
           END-IF
           GOBACK.
