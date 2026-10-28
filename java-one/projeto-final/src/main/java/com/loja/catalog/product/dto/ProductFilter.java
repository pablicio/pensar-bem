package com.loja.catalog.product.dto;

public record ProductFilter(
        String name, Status status, BigDecimal maxPrice) {
}
