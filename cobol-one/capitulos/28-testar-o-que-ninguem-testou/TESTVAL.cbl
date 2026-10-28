       IDENTIFICATION DIVISION.
       PROGRAM-ID. TESTVAL.
      *---------------------------------------------------------------
      * TESTES DO VALCPF. CADA CASO: DOCUMENTO, RETORNO ESPERADO,
      * DESCRICAO. RETURN-CODE 0 SE TODOS PASSAM, 8 SE ALGUM FALHA.
      *---------------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-CASOS-DADOS.
           05  FILLER  PIC X(14) VALUE "123.456.789-09".
           05  FILLER  PIC X(32) VALUE "00VALIDO FORMATADO".
           05  FILLER  PIC X(14) VALUE "12345678909".
           05  FILLER  PIC X(32) VALUE "00VALIDO SEM FORMATACAO".
           05  FILLER  PIC X(14) VALUE "123.456.789-00".
           05  FILLER  PIC X(32) VALUE "03SEGUNDO DIGITO ERRADO".
           05  FILLER  PIC X(14) VALUE "111.111.111-11".
           05  FILLER  PIC X(32) VALUE "02DIGITOS REPETIDOS".
           05  FILLER  PIC X(14) VALUE "000.000.000-00".
           05  FILLER  PIC X(32) VALUE "02SO ZEROS".
           05  FILLER  PIC X(14) VALUE "123.456.78-09".
           05  FILLER  PIC X(32) VALUE "01DEZ DIGITOS".
           05  FILLER  PIC X(14) VALUE SPACES.
           05  FILLER  PIC X(32) VALUE "01EM BRANCO".
           05  FILLER  PIC X(14) VALUE "12345678000195".
           05  FILLER  PIC X(32) VALUE "01CATORZE DIGITOS (CNPJ)".
       01  WS-CASOS REDEFINES WS-CASOS-DADOS.
           05  WS-CASO OCCURS 8 TIMES.
               10  WS-C-DOCUMENTO      PIC X(14).
               10  WS-C-ESPERADO       PIC XX.
               10  WS-C-DESCRICAO      PIC X(30).
       01  WS-I                        PIC 99.
       01  WS-OK                       PIC 99    VALUE 0.
       01  WS-FALHAS                   PIC 99    VALUE 0.
           COPY VALCPFL.
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 8
               INITIALIZE LK-VALCPF
               MOVE WS-C-DOCUMENTO(WS-I) TO LK-DOCUMENTO
               CALL "VALCPF" USING LK-VALCPF
               IF LK-RETORNO = WS-C-ESPERADO(WS-I)
                   ADD 1 TO WS-OK
                   DISPLAY "OK     "
                           FUNCTION TRIM(WS-C-DESCRICAO(WS-I))
               ELSE
                   ADD 1 TO WS-FALHAS
                   DISPLAY "FALHA  "
                           FUNCTION TRIM(WS-C-DESCRICAO(WS-I))
                           " ESPERADO " WS-C-ESPERADO(WS-I)
                           " OBTIDO " LK-RETORNO
               END-IF
           END-PERFORM
           DISPLAY "TESTES: 08  OK: " WS-OK "  FALHAS: " WS-FALHAS
           IF WS-FALHAS > 0
               MOVE 8 TO RETURN-CODE
           END-IF
           GOBACK.
