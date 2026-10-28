        .globl _start
        .text
_start:
        la   s0, cauda
        ld   t0, 0(s0)          # t0 = a primeira posição livre
        li   t1, 230            # a ficha que acabou de chegar
        sh   t1, 0(t0)          # guarda no fim da fila
        addi t0, t0, 2
        sd   t0, 0(s0)          # a próxima livre é a seguinte
        li   a0, 1              # mostra a fila inteira, num write só
        la   a1, fila
        li   a2, 8
        li   a7, 64
        ecall
        li   a0, 0
        li   a7, 93
        ecall

        .data
fila:   .half 214, 215, 219, 0  # a quarta posição está livre
cauda:  .dword fila + 6         # endereço da primeira livre
