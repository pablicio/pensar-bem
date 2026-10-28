        .globl _start
        .text
_start:
        la   t0, ocupados
        lh   t1, 0(t0)          # 31
        slli t3, t1, 1          # 62
        add  t3, t3, t1         # 93
        lh   t2, 2(t0)          # 12
        add  t3, t3, t2         # 105
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
ocupados:      .half 31
acompanhantes: .half 12
total:         .half 0
