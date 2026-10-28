enum Papel: string
{
    case Leitor = 'leitor';
    case Atendente = 'atendente';
    case Admin = 'admin';

    public function permite(Permissao $p): bool
    {
        return in_array($p, $this->permissoes(), true);
    }

    /** @return list<Permissao> */
    public function permissoes(): array
    {
        return match ($this) {
            self::Leitor => [],
            self::Atendente => [
                Permissao::CadastrarAcervo,
                Permissao::VerDadosDeLeitor,
                Permissao::RegistrarCirculacao,
            ],
            self::Admin => Permissao::cases(),
        };
    }
}
