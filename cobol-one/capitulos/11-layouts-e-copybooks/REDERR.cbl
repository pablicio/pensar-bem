       IDENTIFICATION DIVISION.
       PROGRAM-ID. REDERR.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-A                PIC X(8).
       01  WS-B                PIC X(2).
       01  WS-C REDEFINES WS-A PIC 9(8).
       PROCEDURE DIVISION.
           GOBACK.
