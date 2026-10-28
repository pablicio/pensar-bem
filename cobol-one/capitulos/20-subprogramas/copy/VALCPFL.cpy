      *---------------------------------------------------------------
      * VALCPFL - AREA DE COMUNICACAO DO VALCPF (31 BYTES)
      *---------------------------------------------------------------
       01  LK-VALCPF.
           05  LK-DOCUMENTO            PIC X(14).
           05  LK-RETORNO              PIC XX.
               88  CND-CPF-VALIDO                VALUE "00".
           05  LK-CPF-NUMERICO         PIC 9(11).
           05  FILLER                  PIC X(4).
