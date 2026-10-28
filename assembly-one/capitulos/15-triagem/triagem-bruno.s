        .globl _start
        .text
_start:
        la   s7, fichas
        la   s8, cores
inicio:
        la   s4, campos
        li   s5, 3
campo:
        li   s1, 0
tecla_:
        li   a0, 0
        la   a1, tecla
        li   a2, 1
        li   a7, 63
        ecall
        blez a0, desliga
        la   t0, tecla
        lbu  t1, 0(t0)
        li   t2, 42
        beq  t1, t2, invalido
        li   t2, 35
        beq  t1, t2, confirma
        addi t1, t1, -48
        li   t2, 10
        mul  s1, s1, t2
        add  s1, s1, t1
        j    tecla_
confirma:
        sh   s1, 0(s4)
        addi s4, s4, 2
        addi s5, s5, -1
        bnez s5, campo
        la   t0, campos
        lh   t1, 2(t0)
        li   t2, 1
        beq  t1, t2, classifica
        li   t2, 3
        beq  t1, t2, classifica
        li   t2, 4
        beq  t1, t2, classifica
        j    invalido
classifica:
        li   t2, 3
        bne  t1, t2, guarda
        lh   t3, 4(t0)
        li   t2, 80
        blt  t3, t2, guarda
        li   t1, 2
guarda:
        la   t4, quant
        lh   t5, 0(t4)
        li   t2, 5
        bge  t5, t2, cheia
        lh   t3, 0(t0)
        la   t6, fichas
        slli t2, t5, 1
        add  t6, t6, t2
        sh   t3, 0(t6)
        la   t6, cores
        add  t6, t6, t5
        sb   t1, 0(t6)
        addi t5, t5, 1
        sh   t5, 0(t4)
        mv   t2, t5
        li   s3, 5
        li   s6, 0
busca:
        blez t2, mostra
        lbu  t3, 0(s8)
        bge  t3, s3, prox
        mv   s3, t3
        lh   s6, 0(s7)
prox:
        addi s7, s7, 2
        addi s8, s8, 1
        addi t2, t2, -1
        j    busca
mostra:
        mv   t3, s6
        j    exibe
invalido:
        li   t3, 9998
        j    exibe
cheia:
        li   t3, 9997
exibe:
        la   t0, visor
        sh   t3, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        j    inicio
desliga:
        li   a0, 0
        li   a7, 93
        ecall

        .data
campos: .half 0, 0, 0
fichas: .half 0, 0, 0, 0, 0
quant:  .half 0
cores:  .byte 0, 0, 0, 0, 0
tecla:  .byte 0
        .align 1
visor:  .half 0
