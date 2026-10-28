        .globl _start
        .text
_start:
        la   t0, leitos         # t0 aponta para o começo dos dados
        lh   t1, 2(t0)          # t1 = ocupados = 33
        lh   t2, 6(t0)          # t2 = entradas = 2
        add  t1, t1, t2         # t1 = 35
        lh   t2, 8(t0)          # t2 = saidas = 1
        sub  t1, t1, t2         # t1 = 34
        sh   t1, 2(t0)          # ocupados passa a 34
        lh   t2, 0(t0)          # t2 = leitos = 40
        sub  t3, t2, t1         # t3 = 40 - 34 = 6
        sh   t3, 4(t0)          # disponiveis = 6
        li   a0, 1
        addi a1, t0, 4          # endereço de disponiveis
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
leitos:      .half 40           # deslocamento 0
ocupados:    .half 33           # 2
disponiveis: .half 0            # 4
entradas:    .half 2            # 6
saidas:      .half 1            # 8
