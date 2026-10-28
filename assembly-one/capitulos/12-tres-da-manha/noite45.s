        .globl _start
        .text
_start:
        la   s0, eventos
        li   s1, 5
        la   s2, ocupados
laco:
        blez s1, fim
        lbu  t0, 0(s0)
        li   t1, 1
        beq  t0, t1, interna
        li   t1, 2
        beq  t0, t1, alta
        li   t1, 3
        beq  t0, t1, transf
        j    seguinte
alta:
        lh   t2, 0(s2)
        addi t2, t2, -1
        sh   t2, 0(s2)
        j    seguinte
interna:
        lh   t2, 0(s2)
        addi t2, t2, 1
        sh   t2, 0(s2)
        j    seguinte
transf:
        lh   t2, 0(s2)
        addi t2, t2, 1
        sh   t2, 0(s2)
        j    seguinte
seguinte:
        addi s0, s0, 1
        addi s1, s1, -1
        j    laco
fim:
        la   t0, leitos
        lh   t1, 0(t0)
        lh   t2, 0(s2)
        sub  t3, t1, t2
        bltz t3, falha
        bgt  t3, t1, falha
        j    mostra
falha:
        li   t3, 9999
mostra:
        la   t0, livres
        sh   t3, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
eventos:  .byte 2, 1, 3, 2, 1
        .align 1
leitos:   .half 40
ocupados: .half 45
livres:   .half 0
