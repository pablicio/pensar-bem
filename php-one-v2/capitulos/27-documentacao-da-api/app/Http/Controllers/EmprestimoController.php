/**
 * Realiza um empréstimo.
 *
 * Só a equipe empresta; o leitor não empresta para si
 * mesmo pelo aplicativo. O prazo depende do perfil do
 * leitor e é informado em `devolver_ate`.
 */
public function store(
    RealizarEmprestimoRequest $request,
    EmprestimoService $emprestimos,
) {
    // ...
}
