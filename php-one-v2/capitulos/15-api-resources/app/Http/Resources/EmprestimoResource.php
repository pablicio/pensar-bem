public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'status' => $this->status->value,
        'retirado_em' => $this->retirado_em->toIso8601String(),
        'devolver_ate' => $this->devolver_ate->toDateString(),
        'devolvido_em' => $this->devolvido_em?->toIso8601String(),
        'em_atraso' => $this->emAtraso(),
        'multa' => $this->when(
            $this->multa_em_centavos !== null,
            fn () => [
                'centavos' => $this->multa_em_centavos->centavos,
                'formatado' => $this->multa_em_centavos->formatado(),
            ],
        ),
        'exemplar' => new ExemplarResource(
            $this->whenLoaded('exemplar'),
        ),
    ];
}
