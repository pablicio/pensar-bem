public function autores(): BelongsToMany
{
    return $this->belongsToMany(Autor::class)
        ->withPivot('papel')
        ->withTimestamps();
}
