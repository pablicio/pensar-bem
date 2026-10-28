        .globl _start
        .text
_start:
# ---- ler: ficha, cor e idade, cada um terminado por # ----
inicio:
        la   s4, campos         # onde vai o próximo número
        li   s5, 3              # quantos números por paciente
campo:
        li   s1, 0
tecla_:
        li   a0, 0
        la   a1, tecla
        li   a2, 1
        li   a7, 63             # read
        ecall
        blez a0, desliga
        la   t0, tecla
        lbu  t1, 0(t0)
        li   t2, 42             # *: cancela o paciente
        beq  t1, t2, invalido
        li   t2, 35             # #: confirma o número
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
# ---- validar: a cor precisa ser 1, 3 ou 4 ----
        la   t0, campos
        lh   t1, 2(t0)          # cor
        li   t2, 1
        beq  t1, t2, classifica
        li   t2, 3
        beq  t1, t2, classifica
        li   t2, 4
        beq  t1, t2, classifica
        j    invalido
# ---- classificar: amarelo e 80 anos ou mais vira 2 ----
classifica:
        li   t2, 3
        bne  t1, t2, guarda     # não é amarelo
        lh   t3, 4(t0)          # idade
        li   t2, 80
        blt  t3, t2, guarda     # menos de 80
        li   t1, 2              # amarelo prioritário
# ---- guardar, se couber ----
guarda:
        la   t4, quant
        lh   t5, 0(t4)
        li   t2, 5
        bge  t5, t2, cheia      # já há cinco
        lh   t3, 0(t0)          # ficha
        la   t6, fichas
        slli t2, t5, 1          # índice * 2
        add  t6, t6, t2
        sh   t3, 0(t6)
        la   t6, cores
        add  t6, t6, t5         # índice * 1
        sb   t1, 0(t6)
        addi t5, t5, 1
        sh   t5, 0(t4)
# ---- procurar o próximo: reinicia tudo antes ----
        la   t0, fichas
        la   t1, cores
        mv   t2, t5             # contador: quantos na fila
        li   s3, 5              # pior que qualquer cor
        li   s6, 0
busca:
        blez t2, mostra
        lbu  t3, 0(t1)
        bge  t3, s3, prox
        mv   s3, t3
        lh   s6, 0(t0)
prox:
        addi t0, t0, 2
        addi t1, t1, 1
        addi t2, t2, -1
        j    busca
# ---- mostrar e voltar ----
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
campos: .half 0, 0, 0           # ficha, cor, idade do paciente atual
fichas: .half 0, 0, 0, 0, 0     # a fila: até cinco
quant:  .half 0                 # quantos na fila
cores:  .byte 0, 0, 0, 0, 0
tecla:  .byte 0
        .align 1
visor:  .half 0
