        .globl _start
        .text
_start:
        la   t0, dados
        lh   t1, 2(t0)          # ocupados
        lh   t2, 0(t0)          # leitos
        add  t3, t1, t2         # livres
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
dados:  .half 40                # 0 leitos
        .half 31                # 2 ocupados
        .half 0                 # 4 livres
