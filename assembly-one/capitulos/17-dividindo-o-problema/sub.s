        .globl _start
        .text
_start:
        li   a0, 9
        call mostra             # chama; ra recebe a volta
        li   a0, 1
        call mostra             # chama de novo, de outro lugar
        li   a0, 9
        call mostra
        li   a0, 0
        li   a7, 93
        ecall

# ---- mostra: escreve um número no display ----
# entra:  a0 = o número (os 16 bits de baixo)
# sai:    nada
# altera: a0, a1, a2, a7, t0
mostra:
        la   t0, visor
        sh   a0, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        ret                     # volta para quem chamou

        .data
visor:  .half 0
