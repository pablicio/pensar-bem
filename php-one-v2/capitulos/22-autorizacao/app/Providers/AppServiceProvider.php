public function boot(): void
{
    Gate::define(
        'ver-relatorios',
        fn (Usuario $u) => $u->papel !== Papel::Leitor,
    );
}
