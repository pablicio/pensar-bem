@Transactional(readOnly = true)
public List<ProductResponse> listar() {
    return repository.findAll().stream()
            .map(ProductResponse::of)
            .toList();
}

@Transactional
public ProductResponse criar(ProductRequest dados) {
    if (repository.existsByNameIgnoreCase(dados.name())) {
        throw new DuplicateProductException(dados.name());
    }
    Product novo = new Product(
            dados.name(), dados.price(), dados.quantity());
    novo.setDescription(dados.description());
    return ProductResponse.of(repository.save(novo));
}
