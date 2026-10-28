       IDENTIFICATION DIVISION.
       PROGRAM-ID. EXTIPO.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-TIPO-PESSOA      PIC X         VALUE "X".
           88  CND-FISICA                    VALUE "F".
           88  CND-JURIDICA                  VALUE "J".
           88  CND-TIPO-VALIDO               VALUE "F" "J".
       PROCEDURE DIVISION.
           EVALUATE TRUE
               WHEN CND-FISICA
                   DISPLAY "PESSOA FISICA"
               WHEN CND-JURIDICA
                   DISPLAY "PESSOA JURIDICA"
               WHEN NOT CND-TIPO-VALIDO
                   DISPLAY "TIPO INVALIDO: " WS-TIPO-PESSOA
           END-EVALUATE
           GOBACK.
