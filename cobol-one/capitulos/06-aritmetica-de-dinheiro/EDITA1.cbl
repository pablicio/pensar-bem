       IDENTIFICATION DIVISION.
       PROGRAM-ID. EDITA1.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
           DECIMAL-POINT IS COMMA.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-VALOR            PIC S9(7)V99.
       01  WS-ED-Z             PIC ZZZ.ZZZ.ZZ9,99.
       01  WS-ED-MENOS         PIC ----.---.--9,99.
       01  WS-ED-CR            PIC ZZZ.ZZZ.ZZ9,99BCR.
       01  WS-ED-AST           PIC ***.***.**9,99.
       01  WS-ED-DATA          PIC 99/99/9999.
       PROCEDURE DIVISION.
           MOVE 1234567,89 TO WS-VALOR
           PERFORM 1000-MOSTRAR
           MOVE -45,1 TO WS-VALOR
           PERFORM 1000-MOSTRAR
           MOVE 0 TO WS-VALOR
           PERFORM 1000-MOSTRAR
           MOVE 05102026 TO WS-ED-DATA
           DISPLAY "DATA:  [" WS-ED-DATA "]"
           GOBACK.
       1000-MOSTRAR.
           MOVE WS-VALOR TO WS-ED-Z WS-ED-MENOS WS-ED-CR WS-ED-AST
           DISPLAY "Z:     [" WS-ED-Z "]"
           DISPLAY "MENOS: [" WS-ED-MENOS "]"
           DISPLAY "CR:    [" WS-ED-CR "]"
           DISPLAY "AST:   [" WS-ED-AST "]".
