        .globl _start
        .text
_start:
        la   t0, leitos_uti
        lh   t1, 0(t0)          # 12
        lh   t2, 2(t0)          # 9
        sub  t3, t1, t2
        sh   t3, 4(t0)          # livres_uti
        li   a0, 1
        addi a1, t0, 4
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
leitos_uti:   .half 12          # 0
ocupados_uti: .half 9           # 2
livres_uti:   .half 0           # 4
