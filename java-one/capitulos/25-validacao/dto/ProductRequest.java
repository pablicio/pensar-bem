package com.loja.catalog.product.dto;

import jakarta.validation.constraints.*;
import java.math.BigDecimal;

public record ProductRequest(

        @NotBlank(message = "nome é obrigatório")
        @Size(max = 120, message = "nome: até 120 caracteres")
        String name,

        @Size(max = 2000)
        String description,

        @NotNull(message = "preço é obrigatório")
        @Positive(message = "preço deve ser positivo")
        @Digits(integer = 8, fraction = 2)
        BigDecimal price,

        @NotNull
        @PositiveOrZero(message = "estoque não pode ser negativo")
        Integer quantity) {
}
