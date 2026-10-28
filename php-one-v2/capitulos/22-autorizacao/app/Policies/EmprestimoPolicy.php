<?php

declare(strict_types=1);

namespace App\Policies;

use App\Auth\Papel;
use App\Models\Emprestimo;
use App\Models\Usuario;

class EmprestimoPolicy
{
    public function view(Usuario $u, Emprestimo $e): bool
    {
        return $this->ehEquipe($u)
            || $e->leitor_id === $u->leitor_id;
    }

    public function create(Usuario $u): bool
    {
        return $this->ehEquipe($u);
    }

    public function renovar(Usuario $u, Emprestimo $e): bool
    {
        return $this->ehEquipe($u)
            || $e->leitor_id === $u->leitor_id;
    }

    public function devolver(Usuario $u, Emprestimo $e): bool
    {
        return $this->ehEquipe($u);
    }

    private function ehEquipe(Usuario $u): bool
    {
        return in_array(
            $u->papel,
            [Papel::Atendente, Papel::Admin],
            true,
        );
    }
}
