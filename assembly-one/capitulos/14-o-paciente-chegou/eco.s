        .globl _start
        .text
_start:
        li   s1, 0              # o número sendo montado
le:
        li   a0, 0
        la   a1, tecla
        li   a2, 1
        li   a7, 63             # read: uma tecla
        ecall
        blez a0, fim            # nada lido: a entrada acabou
        la   t0, tecla
        lbu  t1, 0(t0)
        li   t2, 35             # o código de #
        beq  t1, t2, fim        # # confirma
        addi t1, t1, -48        # caractere para algarismo
        li   t2, 10
        mul  s1, s1, t2         # empurra uma casa
        add  s1, s1, t1         # e soma o algarismo novo
        j    le
fim:
        la   t0, visor
        sh   s1, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
tecla:  .byte 0
        .align 1
visor:  .half 0
