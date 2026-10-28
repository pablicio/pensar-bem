        .globl _start
        .text
_start:
        la   t0, dados
        lh   s1, 0(t0)          # ocupados: num s, para sobreviver
        lh   t1, 2(t0)          # acompanhantes
        li   t2, 5
        mul  a0, s1, t2
        add  a0, a0, t1
        call mostra
        mv   a0, s1
        call mostra
        li   a0, 0
        li   a7, 93
        ecall

mostra:
        la   t0, visor
        sh   a0, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        ret

        .data
dados:  .half 31, 12
visor:  .half 0
