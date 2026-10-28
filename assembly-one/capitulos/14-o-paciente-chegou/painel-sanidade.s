        .globl _start
        .text
_start:
        la   s2, ocupados
mostra:
        la   t0, leitos
        lh   t1, 0(t0)
        lh   t2, 0(s2)
        sub  t3, t1, t2
        bltz t3, falha          # negativo?
        bgt  t3, t1, falha      # acima de leitos?
        j    guarda
falha:
        li   t3, 9999
guarda:
        la   t0, visor
        sh   t3, 0(t0)
exibe:
        li   a0, 1
        la   a1, visor
        li   a2, 2
        li   a7, 64
        ecall
laco:
        li   a0, 0
        la   a1, tecla
        li   a2, 1
        li   a7, 63
        ecall
        blez a0, desliga
        la   t0, tecla
        lbu  t0, 0(t0)
        li   t1, 49
        beq  t0, t1, entra
        li   t1, 50
        beq  t0, t1, sai
        li   t1, 51
        beq  t0, t1, entra
        li   t3, 9998
        la   t0, visor
        sh   t3, 0(t0)
        j    exibe
entra:
        lh   t2, 0(s2)
        addi t2, t2, 1
        sh   t2, 0(s2)
        j    mostra
sai:
        lh   t2, 0(s2)
        addi t2, t2, -1
        sh   t2, 0(s2)
        j    mostra
desliga:
        li   a0, 0
        li   a7, 93
        ecall

        .data
tecla:    .byte 0
        .align 1
leitos:   .half 40
ocupados: .half 40
visor:    .half 0
