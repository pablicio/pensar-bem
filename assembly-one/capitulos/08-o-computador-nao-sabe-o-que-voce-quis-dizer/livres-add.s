        .globl _start
        .text
_start:
        la   t0, dados
        lh   t1, 0(t0)
        lh   t2, 2(t0)
        add  t3, t1, t2         # o erro do Bruno
        bgt  t3, t1, falha
        j    mostra
falha:
        li   t3, 9999
mostra:
        sh   t3, 4(t0)
        li   a0, 1
        addi a1, t0, 4
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
dados:  .half 40
        .half 31
        .half 0
