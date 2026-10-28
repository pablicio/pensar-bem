package com.loja.catalog.shared.exception;

public record ApiError(
        Instant timestamp,
        int status,
        String error,
        String message,
        String path,
        List<FieldError> fields) {

    public record FieldError(String field, String message) { }
}
