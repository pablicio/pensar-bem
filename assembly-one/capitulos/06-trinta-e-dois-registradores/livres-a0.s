        .globl _start
        .text
_start:
        la   t0, dados
        lh   t1, 2(t0)          # ocupados
        lh   t2, 4(t0)          # bloqueados
        add  t1, t1, t2
        lh   t2, 6(t0)          # reservados
        add  t1, t1, t2         # indisponíveis
        lh   t2, 0(t0)          # leitos
        sub  a0, t2, t1         # a0 = 4, livres
        li   a0, 1              # para onde: o display
        sh   a0, 2(t0)          # guarda os livres... ou não
        addi a1, t0, 2
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
dados:  .half 40                # 0  leitos
        .half 0                 # 2  livres
        .half 31                # 4  ocupados
        .half 3                 # 6  bloqueados
        .half 2                 # 8  reservados
