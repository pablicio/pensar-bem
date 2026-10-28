        .globl _start
        .text
_start:
        la   s2, ocupados
laco:
        li   a0, 0
        la   a1, tecla
        li   a2, 1
        li   a7, 63
        ecall
        blez a0, fim            # a entrada acabou
        la   t0, tecla
        lbu  t0, 0(t0)
        li   t1, 48             # tecla 0: fim do plantão
        beq  t0, t1, fim
        li   t1, 49             # tecla 1: internação
        beq  t0, t1, entra
        li   t1, 50             # tecla 2: alta
        beq  t0, t1, sai
        li   t1, 51             # tecla 3: transferência recebida
        beq  t0, t1, entra
        j    laco               # outro código: ignora
entra:
        lh   t2, 0(s2)
        addi t2, t2, 1
        sh   t2, 0(s2)
        j    laco
sai:
        lh   t2, 0(s2)
        addi t2, t2, -1
        sh   t2, 0(s2)
        j    laco
fim:
        la   t0, leitos
        lh   t1, 0(t0)
        lh   t2, 0(s2)
        sub  t3, t1, t2
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
tecla:    .byte 0
        .align 1
leitos:   .half 40
ocupados: .half 38
livres:   .half 0
