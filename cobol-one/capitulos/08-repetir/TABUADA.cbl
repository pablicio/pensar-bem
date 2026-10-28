       IDENTIFICATION DIVISION.
       PROGRAM-ID. TABUADA.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-I                PIC 9(2).
       01  WS-R                PIC 9(3).
       PROCEDURE DIVISION.
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 10
               COMPUTE WS-R = 7 * WS-I
               DISPLAY "7 X " WS-I " = " WS-R
           END-PERFORM
           GOBACK.
