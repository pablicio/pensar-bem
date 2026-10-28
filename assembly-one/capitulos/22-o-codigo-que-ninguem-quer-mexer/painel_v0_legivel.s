        .globl _start
        .text
_start:
        la   t0, leitos
        lh   t1, 0(t0)          # leitos
        lh   t2, 2(t0)          # ocupados
        sub  t1, t1, t2         # livres
        bgez t1, mostra
        li   t1, 0              # esconde o erro. De propósito? (H.)
mostra:
        sh   t1, 4(t0)
        li   a0, 1
        addi a1, t0, 4
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
leitos:   .half 40              # 0
ocupados: .half 38              # 2
livres:   .half 0               # 4
