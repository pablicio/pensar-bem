        .globl _start
        .text
_start:
        li   a0, 5
        call fatorial
        call mostra
        li   a0, 0
        li   a7, 93
        ecall

# ---- fatorial: n! ----
# entra:  a0 = n (n >= 0)
# sai:    a0 = n!
# altera: a0, t0
fatorial:
        bnez a0, f_recursao
        li   a0, 1              # 0! = 1
        ret
f_recursao:
        addi sp, sp, -16
        sd   ra, 8(sp)
        sd   a0, 0(sp)          # guarda o n desta chamada
        addi a0, a0, -1
        call fatorial           # a0 = (n - 1)!
        ld   t0, 0(sp)          # o n desta chamada
        mul  a0, a0, t0         # n * (n - 1)!
        ld   ra, 8(sp)
        addi sp, sp, 16
        ret

mostra:
        la   t0, visor
        sh   a0, 0(t0)
        li   a0, 1
        mv   a1, t0
        li   a2, 2
        li   a7, 64
        ecall
        ret

        .data
visor:  .half 0
