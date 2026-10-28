        .globl _start
        .text
_start:
        la   s0, acumulado
        li   t1, 155
        li   t3, 0
        li   t4, 7
laco:
        add  t3, t3, t1         # corpo primeiro
        sh   t3, 0(s0)
        li   a0, 1
        mv   a1, s0
        li   a2, 2
        li   a7, 64
        ecall
        addi t4, t4, -1
        bnez t4, laco           # ainda falta? volta
        li   a0, 0
        li   a7, 93
        ecall

        .data
acumulado: .half 0
