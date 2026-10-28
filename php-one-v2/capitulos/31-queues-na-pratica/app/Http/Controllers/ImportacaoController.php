public function show(string $id)
{
    $lote = Bus::findBatch($id) ?? abort(404);

    return [
        'nome' => $lote->name,
        'progresso' => $lote->progress(),
        'pendentes' => $lote->pendingJobs,
        'falhas' => $lote->failedJobs,
        'terminado' => $lote->finished(),
    ];
}
