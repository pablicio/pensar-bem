      *---------------------------------------------------------------
      * LITCTA - CONTAS DO BANCO LITORAL (70 POSICOES) - LAYOUT V1
      *---------------------------------------------------------------
       01  :PFX:-REGISTRO.
           05  :PFX:-AGENCIA           PIC 9(4).
           05  :PFX:-CONTA             PIC 9(7).
           05  :PFX:-DIGITO            PIC X.
           05  :PFX:-NOME              PIC X(22).
           05  :PFX:-DOCUMENTO         PIC X(14).
           05  :PFX:-TIPO-PESSOA       PIC X.
           05  :PFX:-DATA-ABERTURA     PIC 9(6).
           05  :PFX:-SALDO             PIC 9(11)V99.
           05  :PFX:-SINAL             PIC X.
           05  :PFX:-STATUS            PIC X.
