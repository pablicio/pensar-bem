       IDENTIFICATION DIVISION.
       PROGRAM-ID. DUTIL1.
      *---------------------------------------------------------------
      * SOMA N DIAS UTEIS A UMA DATA (FERIADOS BANCARIOS 2027)
      *---------------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-FERIADOS-DADOS.
           05  FILLER  PIC 9(8) VALUE 20270101.
           05  FILLER  PIC 9(8) VALUE 20270208.
           05  FILLER  PIC 9(8) VALUE 20270209.
           05  FILLER  PIC 9(8) VALUE 20270326.
           05  FILLER  PIC 9(8) VALUE 20270421.
           05  FILLER  PIC 9(8) VALUE 20270501.
           05  FILLER  PIC 9(8) VALUE 20270527.
           05  FILLER  PIC 9(8) VALUE 20270907.
           05  FILLER  PIC 9(8) VALUE 20271012.
           05  FILLER  PIC 9(8) VALUE 20271102.
           05  FILLER  PIC 9(8) VALUE 20271115.
           05  FILLER  PIC 9(8) VALUE 20271120.
           05  FILLER  PIC 9(8) VALUE 20271225.
       01  WS-FERIADOS REDEFINES WS-FERIADOS-DADOS.
           05  WS-FERIADO          PIC 9(8) OCCURS 13 TIMES
                                   ASCENDING KEY IS WS-FERIADO
                                   INDEXED BY IX-FER.
       01  WS-DATA                 PIC 9(8).
       01  WS-N                    PIC 9(3).
       01  WS-CONTADOS             PIC 9(3).
       01  WS-DIAS                 PIC 9(7).
       01  WS-SEMANA               PIC 9.
       01  WS-UTIL                 PIC X.
           88  CND-DIA-UTIL                      VALUE "S".
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           MOVE 20270205 TO WS-DATA
           MOVE 3 TO WS-N
           PERFORM 1000-SOMAR-DIAS-UTEIS
           MOVE 20270324 TO WS-DATA
           MOVE 5 TO WS-N
           PERFORM 1000-SOMAR-DIAS-UTEIS
           GOBACK.
       1000-SOMAR-DIAS-UTEIS.
           DISPLAY WS-DATA " + " WS-N " DIAS UTEIS = "
                   WITH NO ADVANCING
           COMPUTE WS-DIAS = FUNCTION INTEGER-OF-DATE(WS-DATA)
           MOVE 0 TO WS-CONTADOS
           PERFORM UNTIL WS-CONTADOS = WS-N
               ADD 1 TO WS-DIAS
               PERFORM 2000-VERIFICAR-DIA
               IF CND-DIA-UTIL
                   ADD 1 TO WS-CONTADOS
               END-IF
           END-PERFORM
           COMPUTE WS-DATA = FUNCTION DATE-OF-INTEGER(WS-DIAS)
           DISPLAY WS-DATA.
       2000-VERIFICAR-DIA.
           MOVE "S" TO WS-UTIL
           COMPUTE WS-SEMANA = FUNCTION MOD(WS-DIAS, 7)
           IF WS-SEMANA = 0 OR WS-SEMANA = 6
               MOVE "N" TO WS-UTIL
           ELSE
               COMPUTE WS-DATA = FUNCTION DATE-OF-INTEGER(WS-DIAS)
               SEARCH ALL WS-FERIADO
                   WHEN WS-FERIADO(IX-FER) = WS-DATA
                       MOVE "N" TO WS-UTIL
               END-SEARCH
           END-IF.
