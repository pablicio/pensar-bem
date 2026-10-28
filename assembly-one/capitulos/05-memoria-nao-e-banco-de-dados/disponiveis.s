        .globl _start
        .text
_start:
        la   t0, leitos         # t0 = endereço de leitos
        lh   t1, 0(t0)          # t1 = 40
        la   t0, ocupados
        lh   t2, 0(t0)          # t2 = 33
        sub  t3, t1, t2         # t3 = 40 - 33
        la   t0, disponiveis
        sh   t3, 0(t0)          # guarda o resultado
mostra:
        li   a0, 1              # mostra no display
        la   a1, disponiveis
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
leitos:      .half 40
ocupados:    .half 33
disponiveis: .half 0
