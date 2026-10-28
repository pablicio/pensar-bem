        .globl _start
        .text
_start:
        la   t0, ocupados
        lh   t1, 0(t0)          # 31
        li   t2, 5
        mul  t3, t1, t2         # t3 = 31 * 5
        sh   t3, 2(t0)          # refeicoes
        li   a0, 1
        addi a1, t0, 2
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
ocupados:  .half 31
refeicoes: .half 0
