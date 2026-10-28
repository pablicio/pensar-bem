@PostMapping
public ResponseEntity<ProductResponse> criar(
        @Valid @RequestBody ProductRequest dados) {
    ...
}
