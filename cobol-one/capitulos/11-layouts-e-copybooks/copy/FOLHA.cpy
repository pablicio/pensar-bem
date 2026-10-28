      *---------------------------------------------------------------
      * FOLHA - ARQUIVO DE REMESSA DE SALARIOS (65 POSICOES)
      * VERSAO 1 - 1998. REGISTROS: 0 HEADER, 1 DETALHE, 9 TRAILER
      *---------------------------------------------------------------
       01  :PFX:-HEADER.
           05  :PFX:-H-TIPO            PIC X.
           05  :PFX:-H-CNPJ            PIC X(14).
           05  :PFX:-H-EMPRESA         PIC X(30).
           05  :PFX:-H-DATA-CREDITO    PIC 9(8).
           05  FILLER                  PIC X(12).
       01  :PFX:-DETALHE.
           05  :PFX:-D-TIPO            PIC X.
           05  :PFX:-D-AGENCIA         PIC 9(4).
           05  :PFX:-D-CONTA           PIC 9(7).
           05  :PFX:-D-DIGITO          PIC X.
           05  :PFX:-D-CPF             PIC 9(11).
           05  :PFX:-D-NOME            PIC X(30).
           05  :PFX:-D-VALOR           PIC 9(9)V99.
       01  :PFX:-TRAILER.
           05  :PFX:-T-TIPO            PIC X.
           05  :PFX:-T-QTD             PIC 9(6).
           05  :PFX:-T-TOTAL           PIC 9(13)V99.
           05  FILLER                  PIC X(43).
