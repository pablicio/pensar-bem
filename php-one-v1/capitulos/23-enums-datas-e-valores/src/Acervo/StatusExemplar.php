    public function disponivel(): bool
    {
        return $this === self::Bom;
    }

    public function rotulo(): string
    {
        return match ($this) {
            self::Bom => 'Disponível',
            self::Emprestado => 'Emprestado',
            self::Restauro => 'Em restauro',
            self::Extraviado => 'Extraviado',
        };
    }
