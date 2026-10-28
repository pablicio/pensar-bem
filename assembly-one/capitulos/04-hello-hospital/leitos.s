        .globl _start
        .text
_start:
        li   a0, 1              # para onde: o display
        la   a1, leitos         # de onde: a meia-palavra leitos
        li   a2, 2              # quantos bytes: dois
        li   a7, 64             # escrever
        ecall
        li   a0, 0
        li   a7, 93             # terminar
        ecall

        .data
leitos: .half 40                # 40, em 16 bits
