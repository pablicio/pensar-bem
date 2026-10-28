package com.loja.catalog.product;

public class ProductNotFoundException extends RuntimeException {
    private final Long id;

    public ProductNotFoundException(Long id) {
        super("produto não encontrado: " + id);
        this.id = id;
    }

    public Long getId() {
        return id;
    }
}
