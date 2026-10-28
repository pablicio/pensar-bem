class LivroPolicy
{
    public function before(Usuario $u, string $habilidade): ?bool
    {
        return $u->papel === Papel::Admin ? true : null;
    }

    public function create(Usuario $u): bool
    {
        return $u->papel === Papel::Atendente;
    }

    public function update(Usuario $u, Livro $livro): bool
    {
        return $u->papel === Papel::Atendente;
    }

    public function delete(Usuario $u, Livro $livro): bool
    {
        return false;
    }
}
