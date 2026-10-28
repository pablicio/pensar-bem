package com.loja.catalog.product;

public class ProductNotFoundException extends RuntimeException {
    public ProductNotFoundException(Long id) {
        super("produto não encontrado: " + id);
    }
}
