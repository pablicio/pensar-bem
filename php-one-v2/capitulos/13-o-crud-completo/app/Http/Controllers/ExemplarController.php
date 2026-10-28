public function destroy(Exemplar $exemplar)
{
    if ($exemplar->estado === StatusExemplar::Emprestado) {
        abort(409, 'Exemplar emprestado não pode ser removido');
    }

    $exemplar->delete();

    return response()->noContent();
}
