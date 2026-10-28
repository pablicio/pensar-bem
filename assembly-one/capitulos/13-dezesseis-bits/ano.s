        .globl _start
        .text
_start:
        la   t0, total
        lh   t1, 0(t0)          # lê com sinal
        bltz t1, falha          # negativo? algo está errado
        j    mostra
falha:
        li   t1, 9999
mostra:
        sh   t1, 2(t0)
        li   a0, 1
        addi a1, t0, 2
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
total:  .half 39412             # atendimentos de 2026
visor:  .half 0
