       IDENTIFICATION DIVISION.
       PROGRAM-ID. ORDEM1.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-A                PIC S9(7)V99  VALUE 100.
       01  WS-B                PIC S9(7)V99  VALUE 3.
       01  WS-C                PIC S9(7)V99.
       PROCEDURE DIVISION.
           COMPUTE WS-C = WS-A / WS-B * WS-B
           DISPLAY "A / B * B = " WS-C
           COMPUTE WS-C = WS-A * WS-B / WS-B
           DISPLAY "A * B / B = " WS-C
           GOBACK.
