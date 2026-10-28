@ExceptionHandler(MethodArgumentNotValidException.class)
public ResponseEntity<ApiError> validacao(
        MethodArgumentNotValidException e,
        HttpServletRequest req) {

    List<ApiError.FieldError> campos = e.getBindingResult()
            .getFieldErrors().stream()
            .map(f -> new ApiError.FieldError(
                    f.getField(), f.getDefaultMessage()))
            .toList();

    ApiError corpo = new ApiError(
            Instant.now(), 400, "Bad Request",
            "dados inválidos", req.getRequestURI(), campos);

    return ResponseEntity.badRequest().body(corpo);
}
