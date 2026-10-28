        .globl _start
        .text
_start:
        la   t0, dados
        lh   t1, 2(t0)          # ocupados
        lh   t2, 4(t0)          # bloqueados
        add  t1, t1, t2
        lh   t2, 6(t0)          # reservados
        add  t1, t1, t2         # t1 = 36, indisponíveis
        sh   t1, 8(t0)
        lh   t2, 0(t0)          # t2 = 40, leitos
        sub  t3, t2, t1         # t3 = 40 - 36
        sh   t3, 10(t0)
        li   a0, 1
        addi a1, t0, 8
        li   a2, 4
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
dados:  .half 40                # 0  leitos
        .half 31                # 2  ocupados
        .half 3                 # 4  bloqueados
        .half 2                 # 6  reservados
        .half 0                 # 8  indisponíveis
        .half 0                 # 10 livres
