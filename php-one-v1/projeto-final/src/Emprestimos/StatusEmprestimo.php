<?php

declare(strict_types=1);

namespace CasaAmarela\Emprestimos;

enum StatusEmprestimo: string
{
    case EmAberto = 'em_aberto';
    case Devolvido = 'devolvido';
    case Renovado = 'renovado';
    case EmAtraso = 'em_atraso';
}
