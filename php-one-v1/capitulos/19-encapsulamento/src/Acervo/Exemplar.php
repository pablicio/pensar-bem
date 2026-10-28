    public function estado(): string
    {
        return $this->estado;
    }

    public function disponivel(): bool
    {
        return $this->estado === 'bom';
    }

    public function emprestar(): void
    {
        if ($this->estado !== 'bom') {
            throw new \RuntimeException(
                "Exemplar {$this->tombo} não sai: {$this->estado}"
            );
        }

        $this->estado = 'emprestado';
    }

    public function devolver(string $estadoNaVolta = 'bom'): void
    {
        if ($this->estado !== 'emprestado') {
            throw new \RuntimeException(
                "Exemplar {$this->tombo} não está emprestado"
            );
        }

        if (!in_array($estadoNaVolta, self::ESTADOS, true)) {
            throw new \InvalidArgumentException(
                "Estado desconhecido: {$estadoNaVolta}"
            );
        }

        $this->estado = $estadoNaVolta;
    }
