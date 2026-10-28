@Tag(name = "Produtos",
     description = "Catálogo da loja")
@RestController
@RequestMapping("/products")
public class ProductController {

    @Operation(
        summary = "Busca um produto pelo id",
        description = "Devolve o produto ativo ou inativo. "
                    + "Não exige autenticação.")
    @ApiResponses({
        @ApiResponse(responseCode = "200",
                     description = "encontrado"),
        @ApiResponse(responseCode = "404",
                     description = "id não existe",
                     content = @Content(schema =
                         @Schema(implementation = ApiError.class)))
    })
    @GetMapping("/{id}")
    public ProductResponse buscar(
            @Parameter(description = "id do produto", example = "7")
            @PathVariable Long id) {
        return service.buscar(id);
    }
}
