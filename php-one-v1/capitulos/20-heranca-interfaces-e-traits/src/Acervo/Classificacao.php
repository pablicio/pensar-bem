    public function prazoEmDias(): int
    {
        if ($this->sonoro) {
            return 21;
        }

        if ($this->infantil) {
            return 7;
        }

        return 14;
    }
