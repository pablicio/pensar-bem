        .globl _start
        .text
_start:
        la   s0, acumulado
        li   t1, 155            # refeições por dia: 31 * 5
        li   t3, 0              # acumulado
        li   t4, 7              # contador: sete dias
laco:
        blez t4, fim            # contador <= 0: acabou
        add  t3, t3, t1         # corpo: acumula o dia
        sh   t3, 0(s0)
        li   a0, 1              #        e mostra
        mv   a1, s0
        li   a2, 2
        li   a7, 64
        ecall
        addi t4, t4, -1         # passo: contador - 1
        j    laco               # volta para o teste
fim:
        li   a0, 0
        li   a7, 93
        ecall

        .data
acumulado: .half 0
