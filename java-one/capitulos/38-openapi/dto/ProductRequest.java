@Schema(description = "Dados para cadastrar um produto")
public record ProductRequest(

        @Schema(description = "Nome exibido no catálogo",
                example = "Teclado mecânico ABNT2")
        @NotBlank @Size(max = 120)
        String name,

        @Schema(description = "Preço de venda em reais",
                example = "349.90")
        @NotNull @Positive
        BigDecimal price,

        @Schema(description = "Unidades em estoque", example = "12")
        @NotNull @PositiveOrZero
        Integer quantity) {
}
