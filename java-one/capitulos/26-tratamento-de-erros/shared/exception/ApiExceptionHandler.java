package com.loja.catalog.shared.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(ProductNotFoundException.class)
    public ResponseEntity<ApiError> naoEncontrado(
            ProductNotFoundException e, HttpServletRequest req) {
        return resposta(HttpStatus.NOT_FOUND, e.getMessage(), req);
    }

    @ExceptionHandler(DuplicateProductException.class)
    public ResponseEntity<ApiError> conflito(
            DuplicateProductException e, HttpServletRequest req) {
        return resposta(HttpStatus.CONFLICT, e.getMessage(), req);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ApiError> requisicaoRuim(
            IllegalArgumentException e, HttpServletRequest req) {
        return resposta(HttpStatus.BAD_REQUEST, e.getMessage(), req);
    }

    private ResponseEntity<ApiError> resposta(
            HttpStatus status, String mensagem,
            HttpServletRequest req) {
        ApiError corpo = new ApiError(
                Instant.now(), status.value(),
                status.getReasonPhrase(), mensagem,
                req.getRequestURI(), List.of());
        return ResponseEntity.status(status).body(corpo);
    }
}
