       IDENTIFICATION DIVISION.
       PROGRAM-ID. SORT1.
      *---------------------------------------------------------------
      * ORDENA O ARQUIVO DO LITORAL POR AGENCIA E CONTA
      *---------------------------------------------------------------
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ARQ-ENTRADA ASSIGN TO LITCTA
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT ARQ-SAIDA ASSIGN TO LITORD
               ORGANIZATION IS LINE SEQUENTIAL.
           SELECT ARQ-TRABALHO ASSIGN TO SORTWK1.
       DATA DIVISION.
       FILE SECTION.
       FD  ARQ-ENTRADA.
       01  ENT-REGISTRO                PIC X(70).
       FD  ARQ-SAIDA.
       01  SAI-REGISTRO                PIC X(70).
       SD  ARQ-TRABALHO.
       01  SRT-REGISTRO.
           05  SRT-AGENCIA             PIC 9(4).
           05  SRT-CONTA               PIC 9(7).
           05  FILLER                  PIC X(59).
       PROCEDURE DIVISION.
       0000-PRINCIPAL.
           SORT ARQ-TRABALHO
               ON ASCENDING KEY SRT-AGENCIA SRT-CONTA
               USING ARQ-ENTRADA
               GIVING ARQ-SAIDA
           IF SORT-RETURN NOT = 0
               DISPLAY "SORT1 - ERRO NA ORDENACAO: " SORT-RETURN
               MOVE 12 TO RETURN-CODE
           END-IF
           GOBACK.
