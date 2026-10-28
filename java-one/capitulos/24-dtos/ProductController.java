@RestController
@RequestMapping("/products")
public class ProductController {

    private final ProductService service;

    public ProductController(ProductService service) {
        this.service = service;
    }

    @GetMapping
    public List<ProductResponse> listar() {
        return service.listar();
    }

    @GetMapping("/{id}")
    public ProductResponse buscar(@PathVariable Long id) {
        return service.buscar(id);
    }

    @PostMapping
    public ResponseEntity<ProductResponse> criar(
            @RequestBody ProductRequest dados) {
        ProductResponse criado = service.criar(dados);
        return ResponseEntity
                .created(URI.create("/products/" + criado.id()))
                .body(criado);
    }
}
