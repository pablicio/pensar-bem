'capa_url' => $this->capa
    ? Storage::disk('public')->url($this->capa)
    : null,
