       IDENTIFICATION DIVISION.
       PROGRAM-ID. REDEF1.
      *---------------------------------------------------------------
      * O COMPLEMENTO DO CADASTRO DE 1987 (PASTA 7)
      *---------------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  CAD-CLIENTE.
           05  CAD-TIPO-PESSOA         PIC X.
               88  CND-PF                        VALUE "F".
               88  CND-PJ                        VALUE "J".
           05  CAD-COMPLEMENTO         PIC X(10).
           05  CAD-COMPL-PF REDEFINES CAD-COMPLEMENTO.
               10  CAD-PF-NASCIMENTO   PIC 9(8).
               10  CAD-PF-SEXO         PIC X.
               10  CAD-PF-ESTADO-CIVIL PIC X.
           05  CAD-COMPL-PJ REDEFINES CAD-COMPLEMENTO.
               10  CAD-PJ-FUNDACAO     PIC 9(8).
               10  CAD-PJ-PORTE        PIC X(2).
       PROCEDURE DIVISION.
           MOVE "F19870315FC" TO CAD-CLIENTE
           PERFORM 1000-MOSTRAR
           MOVE "J19981010ME" TO CAD-CLIENTE
           PERFORM 1000-MOSTRAR
           DISPLAY "TAMANHO DO REGISTRO: " LENGTH OF CAD-CLIENTE
           GOBACK.
       1000-MOSTRAR.
           DISPLAY "COMPLEMENTO: [" CAD-COMPLEMENTO "]"
           EVALUATE TRUE
               WHEN CND-PF
                   DISPLAY "  NASCIMENTO:   " CAD-PF-NASCIMENTO
                   DISPLAY "  SEXO:         " CAD-PF-SEXO
                   DISPLAY "  ESTADO CIVIL: " CAD-PF-ESTADO-CIVIL
               WHEN CND-PJ
                   DISPLAY "  FUNDACAO:     " CAD-PJ-FUNDACAO
                   DISPLAY "  PORTE:        " CAD-PJ-PORTE
           END-EVALUATE.
