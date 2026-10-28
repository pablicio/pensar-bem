protected function casts(): array
{
    return [
        'estado' => StatusExemplar::class,
        'adquirido_em' => 'immutable_date',
    ];
}
