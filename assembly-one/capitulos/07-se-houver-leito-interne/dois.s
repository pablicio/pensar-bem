        .globl _start
        .text
_start:
        la   t0, livres
        lh   t1, 0(t0)
        li   t2, 2
        blt  t1, t2, poucos     # livres < 2
        j    fim                # t1 já tem livres
poucos:
        li   t1, 0
fim:
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
livres:   .half 3
resposta: .half 0
