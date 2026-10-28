class LeitorPolicy
{
    public function view(Usuario $u, Leitor $l): bool
    {
        return $u->leitor_id === $l->id
            || $u->papel->permite(Permissao::VerDadosDeLeitor);
    }

    public function update(Usuario $u, Leitor $l): bool
    {
        return $u->leitor_id === $l->id
            || $u->papel->permite(Permissao::VerDadosDeLeitor);
    }

    public function alterarDocumento(Usuario $u, Leitor $l): bool
    {
        return $u->papel === Papel::Admin;
    }
}
