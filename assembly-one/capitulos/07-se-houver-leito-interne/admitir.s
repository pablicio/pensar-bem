        .globl _start
        .text
_start:
        la   t0, livres
        lh   t1, 0(t0)          # t1 = livres
        blez t1, sem_leito      # livres <= 0: vai para a fila
        addi t1, t1, -1         # interna: livres - 1
        sh   t1, 0(t0)
        lh   t2, 2(t0)
        addi t2, t2, 1          # ocupados + 1
        sh   t2, 2(t0)
        j    fim                # pula o bloco da fila
sem_leito:
        lh   t2, 4(t0)
        addi t2, t2, 1          # na_fila + 1
        sh   t2, 4(t0)
fim:
        li   a0, 1              # mostra livres
        la   a1, livres
        li   a2, 2
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
livres:   .half 4               # 0
ocupados: .half 31              # 2
na_fila:  .half 0               # 4
