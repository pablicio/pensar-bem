return [
    // ...

    /**
     * @deprecated Formato DD/MM/AAAA. Use `devolver_ate_iso`.
     *             Sai em 30/06/2026.
     */
    'devolver_ate' => $this->devolver_ate->format('d/m/Y'),

    'devolver_ate_iso' => $this->devolver_ate->toDateString(),
];
