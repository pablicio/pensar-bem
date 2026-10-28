@ExceptionHandler(AccessDeniedException.class)
public ResponseEntity<ApiError> negado(
        AccessDeniedException e, HttpServletRequest req) {
    return resposta(HttpStatus.FORBIDDEN,
            "acesso negado", req);
}
