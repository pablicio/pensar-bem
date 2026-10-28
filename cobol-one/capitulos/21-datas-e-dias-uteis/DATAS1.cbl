       IDENTIFICATION DIVISION.
       PROGRAM-ID. DATAS1.
      *---------------------------------------------------------------
      * CONVERTE DATAS DDMMAA DO LITORAL PARA AAAAMMDD
      * JANELA: AA >= 72 -> 19AA; AA < 72 -> 20AA. O LITORAL FOI
      * FUNDADO EM 1972. REGRA VALIDA ATE 31/12/2071.
      *---------------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-TESTES-DADOS.
           05  FILLER                  PIC 9(6)  VALUE 150387.
           05  FILLER                  PIC 9(6)  VALUE 050826.
           05  FILLER                  PIC 9(6)  VALUE 300601.
           05  FILLER                  PIC 9(6)  VALUE 310226.
       01  WS-TESTES REDEFINES WS-TESTES-DADOS.
           05  WS-TESTE                PIC 9(6)  OCCURS 4 TIMES.
       01  WS-T                        PIC 9.
       01  WS-DDMMAA.
           05  WS-E-DIA                PIC 99.
           05  WS-E-MES                PIC 99.
           05  WS-E-ANO                PIC 99.
       01  WS-DDMMAA-N REDEFINES WS-DDMMAA PIC 9(6).
       01  WS-DATA.
           05  WS-ANO                  PIC 9(4).
           05  WS-MES                  PIC 99.
           05  WS-DIA                  PIC 99.
       01  WS-DATA-N REDEFINES WS-DATA PIC 9(8).
       01  WS-ED-DATA                  PIC 99/99/9999.
       01  WS-ED-AUX                   PIC 9(8).
       PROCEDURE DIVISION.
           PERFORM VARYING WS-T FROM 1 BY 1 UNTIL WS-T > 4
               MOVE WS-TESTE(WS-T) TO WS-DDMMAA-N
               PERFORM 1000-CONVERTER
           END-PERFORM
           GOBACK.
       1000-CONVERTER.
           IF WS-E-ANO >= 72
               COMPUTE WS-ANO = 1900 + WS-E-ANO
           ELSE
               COMPUTE WS-ANO = 2000 + WS-E-ANO
           END-IF
           MOVE WS-E-MES TO WS-MES
           MOVE WS-E-DIA TO WS-DIA
           IF FUNCTION TEST-DATE-YYYYMMDD(WS-DATA-N) = 0
               COMPUTE WS-ED-AUX = WS-DIA * 1000000
                                 + WS-MES * 10000 + WS-ANO
               MOVE WS-ED-AUX TO WS-ED-DATA
               DISPLAY WS-DDMMAA-N " -> " WS-DATA-N "  " WS-ED-DATA
           ELSE
               DISPLAY WS-DDMMAA-N " -> " WS-DATA-N "  DATA INVALIDA"
           END-IF.
