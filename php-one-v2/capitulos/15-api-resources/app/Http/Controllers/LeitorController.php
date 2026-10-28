public function show(Leitor $leitor)
{
    return new LeitorResource($leitor);
}
