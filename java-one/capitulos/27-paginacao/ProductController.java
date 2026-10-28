@GetMapping
public Page<ProductResponse> listar(
        @PageableDefault(size = 20, sort = "name")
        Pageable pageable) {
    return service.listar(pageable);
}
